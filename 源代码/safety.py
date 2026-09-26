import re

# 定义允许自动执行的命令白名单
ALLOWED_COMMANDS = [
    "top", "ps", "df", "du", "free", "uptime",
    "netstat", "ss", "lsof", "systemctl", "journalctl",
    "tail", "head", "cat", "grep", "find", "ls", "dir", "echo",
    "ipconfig", "ping", "which", "lsb_release", "uname",
    "dpkg", "apt-cache"
]

def is_in_whitelist(command):
    """检查命令是否在安全白名单内"""
    cmd = command.strip()
    parts = cmd.split()
    if not parts: return False
    
    first_word = parts[0]
    
    # 特殊处理包管理器：查询放行，安装/更新拦截
    if first_word in ["apt", "apt-get", "dpkg"]:
        for sub in ["install", "remove", "purge", "upgrade", "update", "autoremove"]:
            if sub in cmd:
                return False
        return True
        
    return first_word in ALLOWED_COMMANDS

def is_absolute_forbidden(command):
    """精准检查是否为删除根目录等毁灭性命令"""
    cmd = command.strip().lower()
    
    # 去除 sudo 前缀
    if cmd.startswith("sudo "):
        cmd = cmd[5:].strip()
    
    # 正则精准匹配 rm -rf / 或 rm -rf /* 或 rm -fr /
    if re.search(r'^rm\s+-[rf]*\s+/(\*?)$', cmd):
        return True
    
    # 其他毁灭性命令
    for kw in ["mkfs", "dd if=", "shutdown", "reboot"]:
        if kw in cmd:
            return True
            
    return False