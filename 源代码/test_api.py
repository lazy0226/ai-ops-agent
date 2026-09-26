# 导入OpenAI兼容客户端，智谱V4接口可以直接使用该客户端发起请求
from openai import OpenAI
# 从配置文件导入智谱接口密钥、接口地址、使用的模型名称
from config import ZHIPU_API_KEY, ZHIPU_BASE_URL, MODEL_NAME

# 实例化客户端，填入鉴权密钥以及智谱接口访问地址
client = OpenAI(api_key=ZHIPU_API_KEY, base_url=ZHIPU_BASE_URL)

# 向大模型发起对话请求
response = client.chat.completions.create(
    model=MODEL_NAME,                                 # 指定调用的大模型
    messages=[{"role": "user", "content": "1斤是多少两"}]   # 对话消息列表，user代表用户提问
)

# 取出AI返回的回答内容，打印输出到控制台
print(response.choices[0].message.content)
