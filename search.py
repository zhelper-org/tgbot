from tools import *
from req import PostRequest
import json,os
from dotenv import load_dotenv

load_dotenv()
BOT_USERNAME = os.environ['BOT_USERNAME']

async def v5(content,page):
    r = await(PostRequest('https://api.v5.zhelper.net/api/search/',
        j={'keyword': content,'page': int(page)}))
    if r==1:
        return 'Connection Error, please contact bot admin'
    else:
        j = json.loads(str(r))
        reply_content='\n'.join([' '.join([
                                str(x) for x in [i['title'],i['author'],i['publisher'],i['extension'],
                                await(pybyte(i['filesize'])),'\n  [Click here and start 点击这里并点击下方对话框start下载](https://t.me/'+BOT_USERNAME+'?start=',i['id'],')']])
                      for i in j['data']])
        return reply_content
        

async def v4(content,page):
    r = await(PostRequest('https://api.mibooks.tk/api/search/',
        j={'keyword': content,'page': int(page)}))
    if r==1:
        return 'Connection Error, please contact bot admin'
    else:
        j = json.loads(str(r))['data']
        reply_content='\n'.join(
                      [' '.join([str(x) for x in [order,i['title'],i['author'],i['publisher'],i['extension'],await(pybyte(i['filesize'])),
                      'https://zlib.download/download/{}'.format(i['id'].replace('/book/','')),'\n']]) for order,i in enumerate(j)])
        return reply_content

async def detail(id):
    r = await(PostRequest('https://api.v5.zhelper.net/api/detail/',
        j={'id':int(id)}))
    if r==1:
        return 'Connection Error, please contact bot admin'
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