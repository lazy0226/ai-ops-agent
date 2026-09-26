import paramiko
from config import VM_HOST, VM_USER, VM_PASSWORD
from safety import is_in_whitelist, is_absolute_forbidden

# 全局授权名单，用户点击“同意”后，命令会被加入这里
APPROVED_COMMANDS = set()

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "在远程Linux服务器上执行一条命令，返回输出结果。用于排查故障。",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "要执行的完整Linux命令行，例如：df -h"
                    }
                },
                "required": ["command"]
            }
        }
    }
]

def execute_remote_command(host, user, password, command):
    """通过 SSH 在虚拟机执行命令"""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"\n🔥 实际连接的IP是: {host} | 用户名是: {user}")
        ssh.connect(host, username=user, password=password, timeout=10)
        stdin, stdout, stderr = ssh.exec_command(command, timeout=15)
        exit_code = stdout.channel.recv_exit_status()
        out = stdout.read().decode('utf-8').strip()
        err = stderr.read().decode('utf-8').strip()
        ssh.close()
        output = out or err or "(无文本输出)"
        if exit_code != 0:
            return f"[命令执行失败，退出码 {exit_code}] 输出：{output}"
        return f"[命令执行成功] 输出：{output}"
    except Exception as e:
        return f"❌ SSH 执行异常: {e}"
    finally:
        ssh.close()

def execute_command(command):
    cmd = command.strip()
    
    # 👇 绝对拦截放到最前面，且不触发弹窗
    if is_absolute_forbidden(cmd):
        print(f"🚨 致命拦截：{cmd}")
        return "❌ 拒绝执行：该命令属于绝对禁止的毁灭性命令（如删除根目录），安全策略强制拦截，且无法通过人工确认放行。"
    
    # 2. 不在白名单内，触发前端弹窗
    if not is_in_whitelist(cmd):
        if cmd in APPROVED_COMMANDS:
            print(f"✅ 用户已授权执行：{cmd}")
            APPROVED_COMMANDS.remove(cmd)
        else:
            print(f"⚠️ 拦截未授权命令：{cmd}")
            return f"[NEED_CONFIRM] {cmd}"
    
    # 3. 通过 SSH 执行
    print(f"📡 正在通过 SSH 将命令发送到虚拟机 {VM_HOST} ...")
    return execute_remote_command(VM_HOST, VM_USER, VM_PASSWORD, cmd)