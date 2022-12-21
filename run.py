from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
import aiohttp
import asyncio
import requests
import json
import os
from tools import  *

load_dotenv()
ZHELPER_BOT_TOKEN = os.environ['ZHELPER_BOT_TOKEN']
LISTEN = os.environ['LISTEN']
PORT = os.environ['PORT']
WEBHOOK_SSL_CERT = os.environ['WEBHOOK_SSL_CERT']
WEBHOOK_SSL_PRIV = os.environ['WEBHOOK_SSL_PRIV']

async def PostRequest(url,j):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url,json=j) as response:
                r=await(response.text())
                if response.ok==0:
                    return 1
                return r
        except aiohttp.ClientConnectorError as e:
            return 1

bot = AsyncTeleBot(ZHELPER_BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
async def send_welcome(message):
    await(bot.reply_to(message, "Search by send '/search keywords', and get download link by send '/detail id'. Besides, you can use /searchv4 to search by zhelper V4 API."))
@bot.message_handler(commands=['search'])
async def search(message):
    r = await(PostRequest('https://api.v5.zhelper.net/api/search/',
        j={'keyword':message.text.split(' ',1)[1]}))
    if r==1:
        await(bot.reply_to(message, 'Connection Error, please contact bot admin'))
    else:
        j = json.loads(str(r))
        try:
            await(bot.reply_to(message, '\n'.join([' '.join([str(x) for x in [i['title'],i['author'],i['publisher'],i['extension'],pybyte(i['filesize']),'/detail',i['id'],]]) for i in j['data']])))
        except:
            await(bot.reply_to(message, 'Connection Error, please contact bot admin'))
@bot.message_handler(commands=['detail'])
async def detail(message):
    r = await(PostRequest('https://api.v5.zhelper.net/api/detail/',
        j={'id':message.text.split(' ',1)[1]}))
    if r==1:
        await(bot.reply_to(message, 'Connection Error, please contact bot admin'))
    else:
        j = json.loads(str(r))
        file_name =j['title']+'_'+j['author']+'.'+j['extension']
        try:
            await(bot.reply_to(message, '\n'.join(['mc_code: {}'.format('{}#{}#{}_{}.{}'.format(j['md5'],j['filesize'],j['title'],j['author'],j['extension'])),'ipfs_id: {}'.format(j['ipfs_cid']),'ipfs_link: https://ipfs.io/ipfs/{}?filename={}'.format(j['ipfs_cid'],file_name),'ipfs_link2: https://dweb.link/ipfs/{}?filename={}'.format(j['ipfs_cid'],file_name),'is_in_libgin: {}'.format(j['in_libgen'])])))
        except:
            await(bot.reply_to(message, 'Connection Error, please contact bot admin'))
            
@bot.message_handler(commands=['searchv4'])
async def search(message):
    r = await(PostRequest('https://api.v4.zhelper.net/api/search/',
        j={'keyword':message.text.split(' ',1)[1]}))
    if r==1:
        await(bot.reply_to(message, 'Connection Error, please contact bot admin'))
    else:
        j = json.loads(str(r))['data']
        try:
            await(bot.reply_to(message, '\n'.join([' '.join([str(x) for x in [order,i['title'],i['author'],i['publisher'],i['extension'],pybyte(i['filesize']),'https://test1.zlib.download/download/{}'.format(i['download_link'].replace('/book/','')),'\n']]) for order,i in enumerate(j)])))
        except:
            await(bot.reply_to(message, 'Connection Error, please contact bot admin'))
    

asyncio.run(bot.run_webhooks(
    listen=LISTEN,
    port=int(PORT),
    certificate=WEBHOOK_SSL_CERT,
    certificate_key=WEBHOOK_SSL_PRIV
))
