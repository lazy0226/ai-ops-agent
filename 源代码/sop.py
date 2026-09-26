import json
import os

# 获取 sop.json 的路径（在项目根目录的 knowledge 文件夹下）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOP_PATH = os.path.join(BASE_DIR, "..", "知识库", "sop.json")

def load_sops():
    """加载所有 SOP 知识库"""
    if not os.path.exists(SOP_PATH):
        return []
    with open(SOP_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def match_sop(text):
    """根据日志内容，匹配最相关的 SOP"""
    sops = load_sops()
    text_lower = text.lower()
    
    for sop in sops:
        for kw in sop["keywords"]:
            if kw.lower() in text_lower:
                return sop  # 匹配到就返回这条 SOP
    return None  # 没匹配到就返回空