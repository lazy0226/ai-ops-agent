from agent import agent_loop

def main():
    print("=" * 50)
    print("  OpsAgent 智能运维助手 v4.0 (记忆优化版)")
    print("  输入 q 退出")
    print("=" * 50)
    
    chat_history = []  # 全局记忆列表
    
    while True:
        print()
        user_input = input("你：").strip()
        
        if user_input.lower() == "q":
            break
        
        # 修复：只拦截空输入，放行“需要”、“好的”等短句
        if not user_input:
            print("⚠️ 输入不能为空，请描述问题！")
            continue
        
        print("\nAgent 正在排查...\n")
        try:
            result = agent_loop(user_input, chat_history)
            print("\n" + "=" * 50)
            print("Agent 最终回复：")
            print(result)
            print("=" * 50)
            
            # 把本次对话存入历史记忆
            chat_history.append({"role": "user", "content": user_input})
            chat_history.append({"role": "assistant", "content": result})
            
        except Exception as e:
            print(f"❌ 出错啦: {e}")

if __name__ == "__main__":
    main()