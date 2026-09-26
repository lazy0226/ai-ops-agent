from openai import OpenAI
from config import ZHIPU_API_KEY, ZHIPU_BASE_URL, MODEL_NAME
from tools import TOOLS, execute_command
from prompts import AGENT_SYSTEM_PROMPT
from sop import match_sop
from logger import AgentLogger
import json
import time

client = OpenAI(api_key=ZHIPU_API_KEY, base_url=ZHIPU_BASE_URL)
logger = AgentLogger()

def agent_loop(user_input, chat_history):
    """Agent 主循环（ReAct + 记忆 + 审计）"""
    session_id = logger.start_session(user_input)
    
    sop = match_sop(user_input)
    sop_hint = ""
    if sop:
        print(f"✅ 命中知识库：{sop['title']}")
        sop_hint = f"\n\n【参考资料（SOP-{sop['code']}）】\n{sop['content']}"
    else:
        print("❌ 未命中知识库，使用 Agent 自主排查...")

    messages = [{"role": "system", "content": AGENT_SYSTEM_PROMPT + sop_hint}]
    messages.extend(chat_history)  
    messages.append({"role": "user", "content": user_input}) 

    for step in range(10):
        response = client.chat.completions.create(
            model=MODEL_NAME, messages=messages, tools=TOOLS
        )
        msg = response.choices[0].message
        
        if not msg.tool_calls:
            logger.end_session(session_id, msg.content)
            return msg.content
        
        tool_call = msg.tool_calls[0]
        command = json.loads(tool_call.function.arguments)["command"]
        thought = msg.content or ""
        
        print(f"\n[步骤 {step+1}] AI 决定执行命令：{command}")
        start_time = time.time()
        result = execute_command(command)
        duration = int((time.time() - start_time) * 1000)
        
        print(f"  -> 执行结果：{result[:150]}...")
        
        # 👇 核心修改：如果触发了安全确认，直接打断循环，把指令返回给前端！
        if "[NEED_CONFIRM]" in result:
            logger.end_session(session_id, result, "need_confirm")
            return result
        
        is_safe = 0 if "拒绝执行" in result else 1
        logger.log_action(session_id, step, command, result, thought, is_safe, duration)
        
        messages.append(msg)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        })
    
    logger.end_session(session_id, "达到最大循环次数", "timeout")
    return "⚠️ 达到最大循环次数，停止排查。"