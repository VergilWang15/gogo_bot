import os
from dotenv import load_dotenv
import telebot
import random

# Load environment variables
load_dotenv()
proxy_settings = ['https_proxy', 'http_proxy', 'all_proxy']
for setting in proxy_settings:
    os.environ[setting] = os.getenv(setting)
BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    print("Received a message: ", message.text)
    replies = ["我刚刚尿沙发上了", "我刚刚尿万里床上了", "我刚刚尿安德床上了", "我刚刚尿老王床上了"]
    bot.reply_to(message, random.choice(replies))

@bot.message_handler(func=lambda message: message.text and '@' + bot.get_me().username.lower() in message.text.lower())
def handle_mention(message):
    responses = ["啊", "啊啊", "啊啊啊"]
    bot.reply_to(message, random.choice(responses))
    
bot.infinity_polling()
