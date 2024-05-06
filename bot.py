import os
from dotenv import load_dotenv
import telebot
import random
import db_utils

# Load environment variables
load_dotenv()
proxy_settings = ['https_proxy', 'http_proxy', 'all_proxy']
for setting in proxy_settings:
    os.environ[setting] = os.getenv(setting)
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# create a bot instance
bot = telebot.TeleBot(BOT_TOKEN)

# create a connection to the database
conn = db_utils.create_connection()
if conn is not None:
    db_utils.create_table(conn)

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

@bot.message_handler(func=lambda message: message.text and '@' + bot.get_me().username.lower() in message.text.lower())
def handle_mention(message):
    responses = ["啊", "啊啊", "啊啊啊"]
    bot.reply_to(message, random.choice(responses))

bot.infinity_polling()
