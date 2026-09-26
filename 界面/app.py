import sys
import os
from flask import Flask, render_template, request, jsonify

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "..", "源代码"))

from agent import agent_loop
from tools import APPROVED_COMMANDS

app = Flask(__name__)
chat_history = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global chat_history
    user_input = request.json.get("message", "")
    confirm_cmd = request.json.get("confirm_command", "")
    confirm_action = request.json.get("confirm_action", "")
    
    if not user_input:
        return jsonify({"reply": "输入不能为空。"})
    
    # 逻辑修复：只有明确点击了“同意”，才把命令加入授权名单
    if confirm_action == 'agree' and confirm_cmd:
        APPROVED_COMMANDS.add(confirm_cmd)
        print(f"✅ 用户已授权执行：{confirm_cmd}")
    elif confirm_action == 'reject':
        # 用户拒绝，直接改写输入，告诉 AI 必须停止
        user_input = "用户拒绝了执行该命令，请立即停止当前任务，不要尝试其他替代命令。"
        print("❌ 用户拒绝了执行。")
    
    try:
        reply = agent_loop(user_input, chat_history)
        
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": reply})
        
        if len(chat_history) > 10:
            chat_history = chat_history[-10:]
        
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"❌ 系统内部错误: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)