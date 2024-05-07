from openai import OpenAI
from dotenv import load_dotenv
import os

# 加载环境配置
def load_configuration(env_file):
    if not os.path.isfile(env_file):
        raise FileNotFoundError("环境配置文件不存在")
    load_dotenv(env_file)
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_API_BASE_URL")
    if not api_key or not base_url:
        raise ValueError("OPENAI_API_KEY 和 OPENAI_API_BASE_URL 必须设置")
    return api_key, base_url

# openai 初始化客户端
def create_openai_client(api_key, base_url):
    return OpenAI(api_key=api_key, base_url=base_url)

# openai 创建聊天消息
def create_chat_messages(messages):
    return [{"role": message['role'], "content": message['message']} for message in messages]

# openai 获取聊天响应
def get_chat_response(client, chat_message, model="gpt-4-turbo", max_tokens=4096, n=1, temperature=0.3):
    return client.chat.completions.create(messages=chat_message, model=model, max_tokens=max_tokens, n=n, temperature=temperature, stream=True)

# 主函数
def chat(sys_messages, user_messages):
    env_file = ".env"
    api_key, base_url = load_configuration(env_file)
    client = create_openai_client(api_key, base_url)

    messages = [
        {'role': 'system', 'message': sys_messages},
        {'role': 'user', 'message': user_messages},
    ]

    chat_messages = create_chat_messages(messages)
    response = get_chat_response(client, chat_messages)
    ouput = ''
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            ouput += chunk.choices[0].delta.content
    return ouput