import os
from dotenv import load_dotenv

# 1. 获取当前 config.py 文件所在的绝对路径（也就是 源代码 文件夹）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. 拼接出项目根目录下的 .env 文件的绝对路径（.. 代表上一级目录）
dotenv_path = os.path.join(BASE_DIR, "..", ".env")

# 3. 显式加载这个绝对路径下的 .env 文件
load_dotenv(dotenv_path=dotenv_path)

# 读取环境变量
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")
ZHIPU_BASE_URL = "https://open.bigmodel.cn/api/paas/v4/"
MODEL_NAME = "glm-4-flash"

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "agent_ops")

# 虚拟机 SSH 配置
VM_HOST = os.getenv("VM_HOST")
VM_USER = os.getenv("VM_USER")
VM_PASSWORD = os.getenv("VM_PASSWORD")