import requests
import json
import rsa
import base64
import re
import time
import random
import threading
import os
import json
# from proxy_server import *

username = "18918969120" #账户名
password = '123456' #密码
bvid_list = []
msg = 0
ifbv = []
headers = {
	"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
}

def rsa_base():
	global dict_1
	url = 'http://passport.bilibili.com/login?act=getkey'
	respones = requests.get(url)
	dict_1 = json.loads(respones.text)
	psd_hash = dict_1["hash"] + password
	rsa_psd_hash = rsa.encrypt(psd_hash.encode("utf-8"),rsa.PublicKey.load_pkcs1_openssl_pem(dict_1["key"]))
	base64_rsa_psd_hash = base64.b64encode(rsa_psd_hash)
	return base64_rsa_psd_hash


def login(username,password): #用户名和密码
	global cookies_1
	url = "https://passport.bilibili.com/web/captcha/combine?plat=6"
	resp = requests.get(url)
	data_1 = json.loads(resp.text)
	print(data_1["data"]["result"]["gt"]) #打开index.html 将本文件返回的gt(第一行)和challenge(第二行)分别填入完成验证，手要快，20秒超时
	print(data_1["data"]["result"]["challenge"])
	psd_rsa_base = rsa_base()
	validate = input("validate:") #点击html文件结果，将validata的数据填入
	seccode = validate + "|jordan"
	datas = {
		"captchaType" : "6" ,
		"username" : username,
		"password" : psd_rsa_base,
		"keep" : "true",
		"key" : data_1["data"]["result"]["key"],
		"challenge" : data_1["data"]["result"]["challenge"],
		"validate" : validate,
		"seccode" : seccode
	}
	respon = requests.post('https://passport.bilibili.com/web/login/v2',data=datas)
	print(respon.text)
	cookies_1 = respon.cookies.items()
	return cookies_1

def comment(message,id): #评论文字和av或bv号
	if "BV" or "bv" in str(id) :
		id = bv_to_av(id)
	SESSDATA = {"SESSDATA":cookies_1[2][1]}
	csrf = cookies_1[3][1]
	data_2 = {
		"type" : "1",
		"oid" : id,
		"message" : message.encode("utf-8"),
		"plat" : "1",
		"csrf" : csrf
	}
	requ = requests.post("http://api.bilibili.com/x/v2/reply/add",cookies=SESSDATA,data=data_2,headers=headers)
	return requ.text

def bv_to_av(x): #bv号转av号
	table='fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
	tr={}
	for i in range(58):
		tr[table[i]]=i
	s=[11,10,3,8,4,6]
	xor=177451812
	add=8728348608
	r=0
	for i in range(6):
		r+=tr[x[s[i]]]*58**i
	return (r-add)^xor

def get(keyword,page): #搜索关键词和获取页数
	# global last_page
	if not os.path.exists("./login"):
		os.makedirs("./login")
	with open("./login/bvid_list.json","w+") as bv:
		bv.write("[]")
	with open("./login/bvid_list.json","r+") as bv:
		ifbv = json.loads(bv.read())
	url = "https://search.bilibili.com/video?keyword={0}&order=pubdate&duration=0&tids_1=0&page={1}".format(keyword,page)
	respon = requests.get(url,headers=headers)
	bvid = re.findall(r'<a href="//www.bilibili.com/video/(.*?)\?from=search.*?" title=".*?" target=".*?" class=".*?">',respon.text)
	# last_page = re.findall(r"[0-9][0-9][\s\S]",re.findall(r'<button class="pagination-btn">([\s\S]*?)</button>',respon.text)[0])[0]
	# last_page = re.findall(r'<button class="pagination-btn">([\s\S]*?)</button>',respon.text)
	# print(last_page)
	for bv in bvid:
		if not bv in bvid_list :
			if not bv in ifbv :
				bvid_list.append(bv)
				ifbv.append(bv)
	with open("./login/bvid_list.json","w") as bv:
		bv.write(json.dumps(ifbv))
	
	# if last_page == str(page):
	# 	msg = 1

def like(aid=None,bvid=None): #选择av号或bv号，av则去除开头av二字直接数字
	csrf = cookies_1[3][1]
	SESSDATA = {"SESSDATA":cookies_1[2][1]}
	url = "http://api.bilibili.com/x/web-interface/archive/like"
	if aid:
		data = {
			"aid" : aid ,
			"like" : "1" ,
			"csrf" : csrf
		}
	elif bvid:
		data = {
			"bvid" : bvid ,
			"like" : "1" ,
			"csrf" : csrf
		}
	respon = requests.post(url,cookies=SESSDATA,headers=headers,data=data)
	return respon.text

#用法示例
print(login(username=username,password=password))
for x in range(1,2)  :
	t1 = threading.Thread(target=get("缘之空",page=x))
	t2 = threading.Thread(target=get("穹",page=x))
	t1.start()
	t2.start()
	time.sleep(0.5)
	print(bvid_list)
	if msg == 1 :
		break
for x in bvid_list:
	print(comment(message="不好意思，有我的地方就有穹",id=x))
	print(like(bvid=x))
	time.sleep(random.randint(3,6))





























