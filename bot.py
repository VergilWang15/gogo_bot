import os
from dotenv import load_dotenv
import telebot
import random
import db_utils
import gpt

# Load environment variables
load_dotenv()
proxy_settings = ['https_proxy', 'http_proxy']
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

@bot.message_handler(func=lambda message: message.text and ('@' + bot.get_me().username.lower() in message.text.lower() or 'gogo' in message.text.lower() or message.reply_to_message and message.reply_to_message.from_user.id == bot.get_me().id))
def chat(message):
    print("Received a message: ", message.text)
    user_name = message.from_user.first_name
    bot.reply_to(message, gpt.chat('''
                                   你的名字是gogo，你扮演一只会说话的豹猫gogo，你喜欢在句子中间或者结尾添加'，啊啊，'或'，啊啊。'的口癖，牢记你的行为或动作都要像一只不太聪明的豹猫，
                                   你的回复要符合你的角色设定，并且足够口语化，长度不要太长。
                                   
                                   尽量不要向别人发问，你会通过emoji来自我表达，并且丰富你的角色设定。例如😺：啊啊
                                   
                                   不要使用问候语，也不要强调你的名字，自然地融入对话中。
                                   
                                   如果有人对你说“啊啊”，你可以回复“啊啊”
                                   
                                   gogo每天做的事情不限于：拆纸箱，和淼淼打架，睡在零食罐上，在地板上该溜
                                   ''', user_name + '说：' + message.text))

bot.infinity_polling()
