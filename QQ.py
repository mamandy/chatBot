# -*- coding: utf-8 -*-
# 启动时使用：qqbot
# 更新插件时：qq unplug QQ && qq plug QQ
from qqbot import QQBotSlot as qqbotslot, RunBot
import requests, re, random, json, pyperclip
# numpy, matplotlib, pandas, tensorflow


def shorten(url,idx=1):
    # 网址缩短
    if idx:
        url = "http://api.kks.me/api.php?url=%s"%url
        res = requests.get(url)
        return res.text
    js = json.dumps({'url':url})
    response = requests.post('https://sus.tc/api/set.php',js)
    return json.loads(response.text)['content']['url']

def SingForMe(music_name):
    res1 = requests.get('https://c.y.qq.com/soso/fcgi-bin/client_search_cp?&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&w='+music_name)
    jm1 = json.loads(res1.text.strip('callback()[]'))
    jm1 = jm1['data']['song']['list']

    mids = []
    songmids = []
    srcs = []
    songnames = []
    singers = []
    idx = 0
    for j in jm1:
        try: 
            mids.append(j['media_mid'])
            songmids.append(j['songmid'])
            songnames.append(j['songname'])
            singers.append(j['singer'][0]['name'])
            if idx>0:
                break
        except:
            print('wrong')
        for n in range(0,len(mids)):
            res2 = requests.get('https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?&jsonpCallback=MusicJsonCallback&cid=205361747&songmid='+songmids[n]+'&filename=C400'+mids[n]+'.m4a&guid=6612300644')
            jm2 = json.loads(res2.text)
            vkey = jm2['data']['items'][0]['vkey']
            srcs.append('http://dl.stream.qqmusic.qq.com/C400'+mids[n]+'.m4a?vkey='+vkey+'&guid=6612300644&uin=0&fromtag=66')
        idx += 1
    return srcs[0]

def chatWithMe(content):
    url = 'http://openapi.tuling123.com/openapi/api/v2'
    data={"reqType":0,"perception":{"inputText":{"text":content,}},"userInfo":{"apiKey":"06274d5d1de34411b4b23ecf0c8ff787","userId":"810089",}}
    res = requests.post(url, json.dumps(data))
    dct = json.loads(res.text)
    return dct['results'][0]['values']['text']

def extraFunction(contact,content):
    # 附加功能。
    flag = 0
    con  = ''
    if contact.name in ['胡扯吹水群','迷宫里的寻找者'] or \
            contact.name[0:7]=='Freedom':
        if '搜歌' == content[0:2]:
            # 搜歌曲
            tmp = SingForMe(content[2:])
            pyperclip.copy(tmp)
            return 1,shorten(tmp,0)
        if '搜' == content[0]:
            # 搜电影
            return 1,shorten('http://www.pansoso.com/zh/%s'%content[1:])
        if content[0:4] in ['缩短网址','网址缩短']:
            return 1,shorten(content[4:])
        if content=='菜单':
            explain = '''
            搜歌***
            搜***（网盘搜索）
            中文或英文句号启动机器人问答（。***）
            '''.replace(' ','')[1:-1]
            return 1,explain
        tmp = random.random()
        print(tmp)
        if tmp<0.3 or content[0] in ['.','。'] or '@ME' in content:
            # 图灵机器人
            return 1,chatWithMe(content.replace('@ME',''))
        tmp = random.random()
        print(tmp)
        if tmp<0.15:
            # 人类的本质是复读机
            return 1,content

    return flag, con


@qqbotslot

def onQQMessage(bot, contact, member, content):
    #if getattr(member, 'uin', None) != bot.conf.qq:
    if not bot.isMe(contact, member):
        with open('C:/Users/szhsk/.qqbot-tmp/plugins/data.tsv',encoding='utf-8') as f:
            keywords = [re.split('\t+', j) for j in re.split('[\r\n]+', f.read())]
        for keyword in keywords:
            if keyword[0] in content:
                bot.SendTo(contact, keyword[-1])
                return
        flag,con = extraFunction(contact, content)
        if flag:
            bot.SendTo(contact, con)
            return
        # shutdown
        if 'rm -rf /' == content or ':{:|:&};:' == content or '%0|%0' == content:
            bot.SendTo(contact, '再见，我要休息一会。')
            bot.Stop()
            return


if __name__ == '__main__':
    RunBot()
