CREATE DATABASE IF NOT EXISTS agent_ops DEFAULT CHARACTER SET utf8mb4;
USE agent_ops;

-- 表1：记录每一次会话（用户问了什么，AI最终答了什么）
CREATE TABLE sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(64) NOT NULL UNIQUE,
    user_input TEXT,
    final_reply TEXT,
    status VARCHAR(20) DEFAULT 'running',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    finished_at DATETIME
);

-- 表2：记录 Agent 的每一步操作（思考、命令、结果）
CREATE TABLE agent_actions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(64) NOT NULL,
    step INT NOT NULL,
    thought TEXT,
    command VARCHAR(1000),
    result TEXT,
    is_safe TINYINT DEFAULT 1,
    duration_ms INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_session (session_id)
);