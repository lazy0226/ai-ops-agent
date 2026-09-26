from openai import OpenAI
from config import ZHIPU_API_KEY, ZHIPU_BASE_URL, MODEL_NAME
from sop import match_sop

client = OpenAI(api_key=ZHIPU_API_KEY, base_url=ZHIPU_BASE_URL)

SYSTEM_PROMPT = """你是一位有10年经验的资深 Linux 运维工程师。
用户会粘贴一段文本，可能只是报错日志，也可能包含了执行的命令和报错日志。

请你按以下逻辑处理：
1. 如果文本里包含命令，请结合命令上下文进行分析。
2. 如果只有报错日志，就按常规分析。
3. 如果文本里只有命令，或者用户明确说“敲了没反应/没报错”，请告诉用户这可能是“静默失败”。不要瞎编报错原因，而是引导用户执行 `echo $?` 检查退出码。

请严格按照以下格式回答：
【问题诊断】一句话说明问题
【可能原因】列出2-3个最可能的原因
【解决步骤】用文字简述操作逻辑
【代码（可直接复制）】给出终端可以逐行执行的命令
【预防建议】如何避免再次发生

注意：
- 如果用户没给命令，不要瞎猜他执行了什么命令。
- 回答要简洁，不超过350字。
"""

def analyze_log(log_text):
    # 1. 去知识库找匹配的 SOP
    sop = match_sop(log_text)
    sop_context = ""
    if sop:
        print(f"✅ 命中知识库：{sop['title']}")  # 终端提示一下，让你看到效果
        sop_context = f"\n\n【参考资料（SOP-{sop['code']}）】\n{sop['content']}"
    else:
        print("❌ 未命中知识库，使用大模型通用知识分析...")
    
    # 2. 拼接上下文，发给大模型
    user_content = f"请分析以下日志：\n{log_text}{sop_context}"
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content}
        ]
    )
    return response.choices[0].message.content