from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
import telebot
import aiohttp
import asyncio
import requests
import json
import os
from tools import *

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
            reply_content='\n'.join([' '.join([
                                    str(x) for x in [i['title'],i['author'],i['publisher'],i['extension'],
                                    await(pybyte(i['filesize'])),'\n  Please Send `/detail',i['id'],'`to get the file']])
                          for i in j['data']])
            await(bot.reply_to(message, reply_content, parse_mode="Markdown"))
        except Exception as e:
            print(str(e))
            await(bot.reply_to(message, 'Unable to find books. Try using other keywords?'))

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
            reply_content = []
            # 转义问题无法解决，会出现 奇怪的效果，见 /detail 3556456，这里先用 行内代码顶一下
            if j.get('md5') and j.get('filesize'):
                rapid_code = '{}#{}#{}_{}.{}'.format(j['md5'],j['filesize'],j['title'],j['author'],j['extension'])
                reply_content.append('*RapidUpload_Code(BaiduNetDisk)*: `https://rapidupload.1kbtool.com/{}`'.format(rapid_code))
            if j.get('ipfs_cid'):
                reply_content.append('*IPFS:*  `https://ipfs-checker.1kbtool.com/{}?filename={}`'.format(j['ipfs_cid'],file_name))
            if j.get('in_libgen') and j.get('md5'):
                reply_content.append('*Libgen* `https://libgendown.1kbtool.com/{}`'.format(j['md5']))
            # if j.get('md5') and j.get('filesize'):
            #     rapid_code = '{}#{}#{}_{}.{}'.format(j['md5'],j['filesize'],j['title'],j['author'],j['extension'])
            #     reply_content.append('*RapidUpload_Code(BaiduNetDisk)*: [RapidUpload GUI](https://rapidupload.1kbtool.com/{})'.format(rapid_code))
            # if j.get('ipfs_cid'):
            #     reply_content.append('*IPFS:* [GATEWAY-Checker](https://ipfs-checker.1kbtool.com/{}?filename={})'.format(j['ipfs_cid'],file_name))
            # if j.get('in_libgen') and j.get('md5'):
            #     reply_content.append('*Libgen*: [Libgen Tool](https://libgendown.1kbtool.com/{})'.format(j['md5']))
            reply_content='\n'.join(reply_content)
            await(bot.reply_to(message, reply_content, parse_mode="Markdown"))
        except:
            await(bot.reply_to(message, 'Connection Error, please contact bot admin'))
            
@bot.message_handler(commands=['searchv4'])
async def search(message):
    r = await(PostRequest('https://api.mibooks.tk/api/search/',
        j={'keyword':message.text.split(' ',1)[1]}))
    if r==1:
        await(bot.reply_to(message, 'Connection Error, please contact bot admin'))
    else:
        j = json.loads(str(r))['data']
        try:
            reply_content='\n'.join(
                          [' '.join([str(x) for x in [order,i['title'],i['author'],i['publisher'],i['extension'],await(pybyte(i['filesize'])),
                          'https://zlib.download/download/{}'.format(i['id'].replace('/book/','')),'\n']]) for order,i in enumerate(j)])
            await(bot.reply_to(message, reply_content))
        except:
            await(bot.reply_to(message, 'Unable to find books. Try using other keywords?'))

async def setcommands():
    await bot.delete_my_commands(scope=None, language_code=None)
    await bot.set_my_commands(
        commands=[
            telebot.types.BotCommand('search', 'search a book through v5'),
            telebot.types.BotCommand('searchv4', 'search a book through mibooks (zhelper V4)'),
            telebot.types.BotCommand('detail', 'get download link')
        ]
    )
    cmd = await bot.get_my_commands(scope=None, language_code=None)
    print([c.to_json() for c in cmd])

asyncio.run(setcommands())


asyncio.run(bot.run_webhooks(
    listen=LISTEN,
    port=int(PORT),
    certificate=WEBHOOK_SSL_CERT,
    certificate_key=WEBHOOK_SSL_PRIV
))
