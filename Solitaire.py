#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2018/08/23 16:31
# @Author : Iydon
# @File   : Solitaire.py
import re,requests, json, random, pypinyin


class solitaire(object):
    """
    Solitaire.
    """

    # ------------CONSTRUCTOR ------------
    def __init__(self, data={"":""}):
        # Private:
        self.__head_data = list(data.keys())
        self.__tail_data = list(data.values())
        self.__length    = len(data)
        self.__data_h    = [[]] * self.__length
        self.__data_t    = [[]] * self.__length
        self.__last      = (0,'')
        #    __options   = list(range(0,len(data)))
        # Process:
        for i in range(0,self.__length):
            with open(file=self.__head_data[i],mode='r',encoding='utf-8') as f:
                self.__data_h[i] = eval(f.read())
            with open(file=self.__tail_data[i],mode='r',encoding='utf-8') as f:
                self.__data_t[i] = eval(f.read())


    # ------------ PUBLIC ------------
    def solo(self,string='',options=[],error_ignore=0):
        string = self.__chinece_only(string)
        if string:
            if not options:
                options = range(0,self.__length)
            if error_ignore:
                if self.__pinyin(string)[0][0]==self.__pinyin(self.__last[1])[-1][0]:
                    return self.__think_out(self.__pinyin(string)[-1][0],options)
                else:
                    return False
            else:
                pass
        else:
            if options:
                idx1 = self.__random(options)
            else:
                idx1 = self.__random(range(0,self.__length))
            dct  = self.__data_t[idx1]
            key  = self.__random(dct.keys())
            if dct[key]:
                idx2 = self.__random(dct[key],idx_falg=1)
                tmp  = dct[key][idx2]
                self.__data_t[idx1][key] = dct[key][:idx2]+dct[key][idx2+1:]
                self.__last = (idx1,tmp)
                return tmp
            else:
                return self.solo(string,options)

    def meaning(self,string):
        return self.__meaning(string,dct2str=1)



    # ------------ PRIVATE ------------
    def __think_out(self,pinyin,options):
        options = list(options)
        idx1 = self.__random(options)
        if pinyin in self.__data_t[idx1].keys():
            lsts = self.__data_t[idx1][pinyin]
            if lsts:
                idx2 = self.__random(lsts,idx_falg=1)
                tmp = lsts[idx2]
                self.__data_t[idx1][pinyin] = lsts[:idx2]+lsts[idx2+1:]
                self.__last = (idx1,tmp)
                return tmp
            else:
                return self.__think_out(pinyin,set(options).difference([idx1]))
        else:
            return self.__think_out(pinyin,set(options).difference([idx1]))
        pass

    def __pinyin(self,string):
        string = self.__chinece_only(string)
        py = self.__deleteTone(pypinyin.pinyin(string))
        return py

    def __random(self,lst,idx_falg=0):
        lst = list(lst)
        idx = random.randint(0,len(lst)-1)
        return idx if idx_falg else lst[idx]

    def __chinece_only(self,string):
        return re.sub('[^一-龥]','',string)

    def __meaning(self,string,dct2str=0):
        url = "https://api.aijielong.cn/idiom/word?name=%s"%(string)
        response = requests.get(url)
        dct = json.loads(response.text)
        if dct2str:
            if dct['status']:
                data = dct["data"]
                string = "%s: %s\n含义: %s\n出处: %s\n例子: %s"% \
                    (data["name"],data["pinyin"],data["meaning"], \
                        data["provenance"],data["example"])
                return string
            else:
                return dct["error"]
        else:
            return dct

    def __deleteTone(self,string):
        if isinstance(string,str):
            lists = [
                ["āáǎà",  "a"],
                ["ōóǒò",  "o"],
                ["ēéěèê", "e"],
                ["īíǐì",  "i"],
                ["ūúǔùü", "u"],
                ["ńň",   "n"],
                ["",     "m"],
                ["0123456789", ""]
            ]
            for lst in lists:
                for ele in lst[0]:
                    string = string.replace(ele,lst[-1])
            return string
        else:
            tmp = []
            for val in string:
                tmp.append(self.__deleteTone(val))
            return tmp



def solitaire_plus(Solitairer,ans):
    if ans[:2]=="提示":
        print(ans[2:])
        try:
            return Solitairer._solitaire__think_out(ans[2:],[0,1,2])
        except:
            return "提示出错啦~"
    if ans:
        if len(ans)<4:
            return "不知是不是成语呢~"
        elif len(ans)==4:
            if ans in Solitairer._solitaire__data_h[0].keys():
                tmp = Solitairer.solo(string=ans, error_ignore=1)
                if tmp:
                    try:
                        return Solitairer.meaning(ans)+'\n\n'+tmp
                    except:
                        return tmp
                else:
                    return "读音貌似接不上呢~"
            else:
                return "不在我的数据库呢~"
        else:
            tmp = Solitairer.solo(string=ans, error_ignore=1)
            return tmp if tmp else ans+"读音貌似接不上呢~"
    else:
        return "输入不能为空~"