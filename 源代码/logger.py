import pymysql
import uuid
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

class AgentLogger:
    def __init__(self):
        try:
            self.conn = pymysql.connect(
                host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
                database=DB_NAME, charset="utf8mb4", autocommit=True
            )
        except Exception as e:
            print(f"⚠️ 数据库连接失败，审计功能关闭。错误：{e}")
            self.conn = None

    def start_session(self, user_input):
        """开始一次会话，返回 session_id"""
        if not self.conn: return "offline_session"
        session_id = str(uuid.uuid4())
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO sessions (session_id, user_input) VALUES (%s, %s)",
                (session_id, user_input)
            )
        return session_id

    def log_action(self, session_id, step, command, result, thought="", is_safe=1, duration_ms=0):
        """记录 Agent 的一步操作"""
        if not self.conn: return
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO agent_actions 
                       (session_id, step, thought, command, result, is_safe, duration_ms)
                       VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                    (session_id, step, thought, command, result[:5000], is_safe, duration_ms)
                )
        except Exception as e:
            print(f"[审计日志写入失败] {e}")

    def end_session(self, session_id, final_reply, status="success"):
        """结束会话，更新最终结果"""
        if not self.conn: return
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE sessions SET final_reply=%s, status=%s, finished_at=NOW() WHERE session_id=%s",
                (final_reply, status, session_id)
            )