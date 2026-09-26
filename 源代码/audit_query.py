from logger import AgentLogger

def show_recent_sessions(limit=5):
    """查看最近的会话记录"""
    logger = AgentLogger()
    if not logger.conn:
        return
        
    print("\n===== 最近的会话记录 =====")
    with logger.conn.cursor() as cur:
        cur.execute("""
            SELECT session_id, user_input, status, created_at
            FROM sessions ORDER BY created_at DESC LIMIT %s
        """, (limit,))
        for row in cur.fetchall():
            print(f"[{row[3]}] 状态: {row[2]}")
            print(f"  用户: {row[1][:40]}")
            print(f"  ID:   {row[0]}")
            print("-" * 40)

def show_actions(session_id):
    """查看某次会话中，AI 到底执行了什么"""
    logger = AgentLogger()
    print(f"\n===== AI 执行细节 (Session: {session_id[:8]}...) =====")
    with logger.conn.cursor() as cur:
        cur.execute("""
            SELECT step, command, result, is_safe, duration_ms
            FROM agent_actions WHERE session_id = %s ORDER BY step
        """, (session_id,))
        for row in cur.fetchall():
            safe_tag = "✅" if row[3] else "❌ 被拦截"
            print(f"[步骤{row[0]}] {safe_tag} 耗时{row[4]}ms")
            print(f"  AI 命令: {row[1]}")
            print(f"  执行结果: {row[2][:100]}...")
            print("-" * 40)

if __name__ == "__main__":
    show_recent_sessions()
    # 你可以把上面打印出来的某个 session_id 复制到这里，查看细节
    # show_actions("这里粘贴session_id")