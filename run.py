from dotenv import load_dotenv
import telebot
import requests
import json
import os

load_dotenv()
ZHELPER_BOT_TOKEN = os.environ['ZHELPER_BOT_TOKEN']
TELEGRAM_GATEWAY = os.environ['TELEGRAM_GATEWAY']
LISTEN = os.environ['LISTEN']
PORT = os.environ['PORT']
WEBHOOK_SSL_CERT = os.environ['WEBHOOK_SSL_CERT']
WEBHOOK_SSL_PRIV = os.environ['WEBHOOK_SSL_PRIV']

bot = telebot.TeleBot(ZHELPER_BOT_TOKEN) # You can set parse_mode by default. HTML or MARKDOWN


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Search by send '/search keywords', and get download link by send '/detail id'. Besides, you can use /searchv4 to search by zhelper V4 API.")
@bot.message_handler(commands=['search'])
def search(message):
    r = requests.post('https://api.v5.zhelper.net/api/search/',json={'keyword':message.text.split(' ',1)[1]})
    j = json.loads(r.text)
    bot.reply_to(message, '\n'.join([' '.join([str(x) for x in [i['title'],i['author'],i['publisher'],i['extension'],i['filesizeString'],'/detail',i['zlibrary_id'],]]) for i in j]))

@bot.message_handler(commands=['detail'])
def detail(message):
    r = requests.post('https://api.v5.zhelper.net/api/detail/',json={'id':str(message.text.split(' ',1)[1])})
    j = json.loads(r.text)
    file_name =j['title']+'_'+j['author']+'.'+j['extension']
    bot.reply_to(message, '\n'.join(['mc_code: {}'.format(j['mc']),'ipfs_id: {}'.format(j['ipfs_cid']),'ipfs_link: https://ipfs.io/ipfs/{}?filename={}'.format(j['ipfs_cid'],file_name),'ipfs_link2: https://dweb.link/ipfs/{}?filename={}'.format(j['ipfs_cid'],file_name),'is_in_libgin: {}'.format(j['in_libgen'])]))

@bot.message_handler(commands=['searchv4'])
def search(message):
    r = requests.post('https://api.v4.zhelper.net/api/search/',json={'keyword':message.text.split(' ',1)[1]})
    j = json.loads(r.text)
    bot.reply_to(message, '\n'.join([' '.join([str(x) for x in [order,i['title'],i['author'],i['publisher'],i['extension'],i['filesizeString'],'https://download.zhelper.de/download/{}/{}'.format(i['id'],i['hash']),'\n']]) for order,i in enumerate(j)]))

bot.run_webhooks(
    listen=LISTEN,
    port=int(PORT),
    certificate=WEBHOOK_SSL_CERT,
    certificate_key=WEBHOOK_SSL_PRIV
)
