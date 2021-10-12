import telebot
from telebot.types import Message
import random
import re
import requests
import os
from datetime import datetime
import time

if not os.path.isdir('album'):
    os.mkdir('album')
ospath=''
if os.name == 'nt':
    ospath='album\\'
else: ospath='album/'

def tokenTGget():
    with open('tokentg.txt','r') as tokenfile:
        return tokenfile.read()
def tokenAIget():
    with open('tokenai.txt','r') as tokenfile:
        return tokenfile.read()

TOKENTG = tokenTGget().rstrip()
bot = telebot.TeleBot(TOKENTG)
print('Send me a link from instagram. And i will put image to album.')

@bot.message_handler(content_types=['text'])
@bot.edited_message_handler(content_types=['text'])
def send_echo(message):

    if "instagram" in message.text:
        try:
            urljunk =  re.findall(r"\?.*",message.text)[0]
            url = message.text.replace(urljunk,"media?size=l")
            bot.send_message(message.chat.id, url)
            mtime = int(datetime.now().timestamp())
            microtime = str(mtime)
            with requests.Session() as s:
                r=s.get(url,allow_redirects=True,headers={"User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Mobile Safari/537.36"})
                time.sleep(2)
                out = open(f'{ospath}{microtime}_{random.randint(0,99)}.jpg', 'wb')
                out.write(r.content)
                out.close()
        except:bot.send_message(message.chat.id, "Something wrong with link. Try again")
    else:
        bot.send_message(message.chat.id, 'Send me a link from instagram.')
    

print('Running')
bot.polling( none_stop = True)
