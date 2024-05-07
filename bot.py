import os
from dotenv import load_dotenv
import telebot
import random
import db_utils
import gpt
import yaml
import tokenizer
# Load environment variables
load_dotenv()
proxy_settings = ['https_proxy', 'http_proxy']
for setting in proxy_settings:
    os.environ[setting] = os.getenv(setting)
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# Load the prompts from the prompts.yaml file
with open('prompts.yaml', 'r') as file:
    preset_prompt = yaml.safe_load(file)
    
# create a bot instance
bot = telebot.TeleBot(BOT_TOKEN)

# create a connection to the database
conn = db_utils.create_connection()
if conn is not None:
    db_utils.create_table(conn)

# chat context
chat_contexts = {}

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    print("Received a message: ", message.text)
    replies = ["尿沙发", "尿万里床", "尿安德床", "尿老王床"]
    bingo = random.choice(replies)
    bot.reply_to(message, "我刚刚" + bingo + "上了")
    db_utils.update_command_count(conn, bingo)

@bot.message_handler(commands=['count'])
def send_count(message):
    print("Received a message: ", message.text)
    c = conn.cursor()
    c.execute("SELECT * FROM commands")
    rows = c.fetchall()
    response = ""
    for row in rows:
        response += f"{row[1]}: {row[2]} 次\n"
    bot.reply_to(message, response)

@bot.message_handler(func=lambda message: True)
def update_context(message):
    print("Received a message: ", message.text)
    user_name = message.from_user.first_name
    chat_id = message.chat.id

    # 每次收到消息时，都将消息添加到对应聊天的上下文中
    if chat_id not in chat_contexts:
        chat_contexts[chat_id] = []
    
    # 检查上下文的长度
    context = ' '.join(chat_contexts[chat_id])
    if tokenizer.num_tokens_from_messages([{'role': 'user', 'message': context}]) > 1000:
        # 如果上下文的长度超过了1000个token，那么获取上下文的摘要
        summary = gpt.chat(preset_prompt['summary'], context)
        chat_contexts[chat_id] = [summary]
    
    # 将用户的名称和消息一起添加到上下文中
    chat_contexts[chat_id].append(user_name + '说：' + message.text)
    # 对话
    chat(message)

def chat(message):
    # 检查消息是否满足特定的条件
    if message.text and ('@' + bot.get_me().username.lower() in message.text.lower() or 'gogo' in message.text.lower() or message.reply_to_message and message.reply_to_message.from_user.id == bot.get_me().id):
        user_name = message.from_user.first_name
        chat_id = message.chat.id
        # 在生成回复时，使用当前聊天的上下文
        context = ' '.join(chat_contexts[chat_id])
        bot.reply_to(message, gpt.chat(preset_prompt['gogo_system_msg'], user_name + '说：' + context))

bot.infinity_polling()
