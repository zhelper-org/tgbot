from dotenv import load_dotenv
import os
from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot
import asyncio
from search import *

load_dotenv()
ZHELPER_BOT_TOKEN = os.environ['ZHELPER_BOT_TOKEN']
LISTEN = os.environ['LISTEN']
PORT = os.environ['PORT']
WEBHOOK_SSL_CERT = os.environ['WEBHOOK_SSL_CERT']
WEBHOOK_SSL_PRIV = os.environ['WEBHOOK_SSL_PRIV']

bot = AsyncTeleBot(ZHELPER_BOT_TOKEN)

async def extract_unique_code(text):
    return text.split()[1] if len(text.split()) > 1 else None

@bot.message_handler(commands=['start'])
async def send_welcome(message):
    unique_code = await extract_unique_code(message.text)
    if unique_code: 
        r = await(PostRequest('https://api.v5.zhelper.net/api/detail/',
            j={'id':unique_code}))
        if r==1:
            await(bot.reply_to(message, 'Connection Error, please contact bot admin. \n\n连接出错，请联系管理员'))
        else:
            j = json.loads(str(r))
            file_name =j['title']+'_'+j['author']+'.'+j['extension']
            try:
                reply_content='\n'.join(['*RapidUpload_Code(BaiduNetDisk)*: `{}`'.format('{}#{}#{}_{}.{}'.format(j['md5'],j['filesize'],j['title'],j['author'],j['extension'])),
                                         '*IPFS_ID:* `{}`'.format(j['ipfs_cid']),
                                         '*IPFS_PUBLIC_GATEWAY0:* [LINK0(IPFS.IO)](https://ipfs.io/ipfs/{}?filename={})'.format(j['ipfs_cid'],file_name),
                                         '*IPFS_PUBLIC_GATEWAY1:* [LINK1(DWEB.LINK)](https://dweb.link/ipfs/{}?filename={})'.format(j['ipfs_cid'],file_name),
                                         '*WHETHER_FILE_IN_LIBGEN:* {}'.format(j['in_libgen'])])
                await(bot.reply_to(message, reply_content, parse_mode="Markdown"))
            except:
                await(bot.reply_to(message, 'Connection Error, please contact bot admin'))
    else:
        reply = """Welcome to Zhelper bot! Please type your book name and we will find the book for you.
zhelper international group: https://t.me/zhelperorg
欢迎使用zhelper机器人！请直接输入书名进行搜索。zhelper官方中文群https://t.me/zhelpert"""
    await bot.reply_to(message, reply)

@bot.message_handler(commands=['help'])
async def send_welcome(message):
    await(bot.reply_to(message, """Welcome to Zhelper bot! Please type your book name and we will find the book for you.
zhelper international group: https://t.me/zhelperorg
欢迎使用zhelper机器人！请直接输入书名进行搜索。zhelper官方中文群https://t.me/zhelpert"""))

async def gen_markup(t):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("(local database) 离线数据库", callback_data="v5."+t+".1"))
    markup.add(InlineKeyboardButton("(online database)在线数据库", callback_data="v4."+t+".1"))
    return markup
async def gen_page_markup(method,t,page):
    markup = InlineKeyboardMarkup()
    if page!="1": 
        markup.add(InlineKeyboardButton("<-", callback_data="v5."+t+"."+str(int(page)-1)),
                   InlineKeyboardButton(page,callback_data="ignore"),
                   InlineKeyboardButton("->", callback_data=method+t+"."+str(int(page)+1)))
    else:
        markup.add(InlineKeyboardButton("<-", callback_data="ignore"),
                   InlineKeyboardButton(page,callback_data="ignore"),
                   InlineKeyboardButton("->", callback_data=method+t+"."+str(int(page)+1)))
    return markup

@bot.callback_query_handler(func=lambda call: True)
async def callback_query(call):
    data=call.data
    if data=="ignore":
        return
    command=data.split('.')[0]
    content=data.split('.')[1]
    page=data.split('.')[2]
    if command == "v4":
        reply_content=await v4(content,page)
        try:
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=reply_content, reply_markup=await gen_page_markup('v4.',content,page),parse_mode='Markdown')
        except Exception as e:
            print(str(e))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Unable to find books. Try using other keywords?\n我们无法找到这本书，请尝试更换关键词')
    elif command == "v5":
        reply_content=await v5(content,page)
        try:
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=reply_content, reply_markup=await gen_page_markup('v5.',content,page),parse_mode='Markdown')
        except Exception as e:
            print(str(e))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Unable to find books. Try using other keywords?\n我们无法找到这本书，请尝试更换关键词')
@bot.message_handler(func=lambda message: True)
async def allmessage(message):
    await bot.reply_to(message, "Please choose the database\n请选择数据库", reply_markup=await gen_markup(message.text))


# asyncio.run(setcommands())
asyncio.run(bot.run_webhooks(
    listen=LISTEN,
    port=int(PORT),
    certificate=WEBHOOK_SSL_CERT,
    certificate_key=WEBHOOK_SSL_PRIV
))