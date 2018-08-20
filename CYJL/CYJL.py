# -*- coding: utf-8 -*-
import re, pypinyin, random


global PRO1, PRO2, AED, last

with open(file='CYJL_P1',encoding='utf-8') as f:
	PRO1 = eval(f.read())
	keys = list(PRO1.keys())
with open(file='CYJL_P2',encoding='utf-8') as f:
	PRO2 = eval(f.read())
AED = []
last = ''


def chengyujielong(enter=''):
	global PRO1, PRO2, AED, last
	with open('CYJL_pre','r',encoding='utf-8') as f:
		pre = f.read().strip().split('\n')
	with open('CYJL_post','r',encoding='utf-8') as f:
		pos = f.read().strip().split('\n')
	if enter:
		if enter=='提示嘛~':
			# 提示
			if PRO1[PRO2[last]]:
				# 尚有提示
				randidx3 = random.randint(0,len(PRO1[PRO2[last]])-1)
				PRO1[PRO2[last]] = removeIf(PRO1[PRO2[last]], PRO1[PRO2[last]][randidx3])
				last = PRO1[PRO2[last]][randidx3]
				AED.append(last)
				return last
			else:
				return 'I vegetable exploded...'
		elif len(enter)==4:
			# 默认是成语
			if enter in PRO2.keys():
				# 属于成语
				if PRO2[last]==re.sub('\d','',pypinyin.pinyin(enter,style=pypinyin.Style.TONE2)[0][0]):
					if PRO1[PRO2[enter]]:
						# 存在回答内容
						if enter not in AED:
							# 没有回答过
							randidx4 = random.randint(0,len(PRO1[PRO2[enter]])-1)
							PRO1[PRO2[last]] = removeIf(PRO1[PRO2[enter]], PRO1[PRO2[enter]][randidx4])
							last = PRO1[PRO2[enter]][randidx4]
							AED.append(enter)
							return '%s%s%s'%(pre[random.randint(0,len(pre)-1)],last,pos[random.randint(0,len(pos)-1)])
						else:
							# 回答过
							return '回答过的话~'
					else:
						# 没有回答内容
						return '稽不如人，肝拜下风~'
				else:
					# 没有接上
					return '有内鬼，终止交易~'
			else:
				# 不属于成语
				return '虽然我不知道原因，但肯定有问题~'
		else:
			# 默认不是成语
			return None
	else:
		# 随即返回
		randidx1 = random.randint(0,len(PRO1.keys())-1)
		if PRO1[keys[randidx1]]:
			randidx2 = random.randint(0,len(PRO1[keys[randidx1]])-1)
			last = PRO1[keys[randidx1]][randidx2]
			AED.append(last)
			PRO1[keys[randidx1]] = removeIf(PRO1[keys[randidx1]], last)
			return last
		else:
			return '脑阔痛，想不出来了QAQ'

def removeIf(lst, name):
	idx = lst.index(name)
	return lst[:idx]+lst[idx+1:]

while True:
	print(chengyujielong(input('E: ')))