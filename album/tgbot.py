import telebot
from telebot.types import Message
import random
import re
import requests

from datetime import datetime
import time

def tokenTGget():
    with open('tokentg.txt','r') as tokenfile:
        return tokenfile.read()
def tokenAIget():
    with open('tokenai.txt','r') as tokenfile:
        return tokenfile.read()

TOKENTG = tokenTGget().rstrip()
bot = telebot.TeleBot(TOKENTG)


@bot.message_handler(content_types=['text'])
@bot.edited_message_handler(content_types=['text'])
def send_echo(message):

    if "instagram" in message.text:
        try:
            urljunk =  re.findall(r"\?.*",message.text)[0]
            url = message.text.replace(urljunk,"media?size=l")
            bot.send_message(message.chat.id, url)
        except:bot.send_message(message.chat.id, "Что-то не так с ссылкой.")
    else:
        bot.send_message(message.chat.id, 'Кинь мне ссылку на пост в инсте, я ее переделаю.')
    mtime = int(datetime.now().timestamp())
    microtime = str(mtime)
    with requests.Session() as s:
        r=s.get(url,allow_redirects=True,headers={"User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Mobile Safari/537.36"})
        time.sleep(2)
        out = open(f'{microtime}_{random.randint(0,9)}.jpg', 'wb')
        out.write(r.content)
        out.close()


bot.polling( none_stop = True)
