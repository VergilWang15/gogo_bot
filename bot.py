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
    replies = ["我刚刚尿沙发上了", "我刚刚尿万里床上了", "我刚刚尿安德床上了", "我刚刚尿老王床上了"]
    bot.reply_to(message, random.choice(replies))

bot.infinity_polling()