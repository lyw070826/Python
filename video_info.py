

import json
try:
    from proxy_s_erver import *
except Exception as e:
    import requests
    proxy_ok = {}
    headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    }
try:
    from avb_v import av_to_bv
except Exception as e:
    table='fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
    tr={}
    for i in range(58):
        tr[table[i]]=i
    s=[11,10,3,8,4,6]
    xor=177451812
    add=8728348608
    def av_to_bv(x):
        x=(x^xor)+add
        r=list('BV1  4 1 7  ')
        for i in range(6):
            r[s[i]]=table[x//58**i%58]
        return ''.join(r)


##############################################################


class video_info(object):
    """docstring for bilibili video_info"""
    def __init__(self):
        super(video_info, self).__init__()
        self.url_bv = "https://api.bilibili.com/x/web-interface/view?bvid="
        self.error_msg_1 = '{"code":-404,"message":"啥都木有","ttl":1}'
        self.error_msg_2 = '{"code":-400,"message":"请求错误","ttl":1}'

    def get_video_info(self,av_or_bv):
        global video_data
        if "av" in av_or_bv :
            av = av_or_bv[2:]
            bv = av_to_bv(int(av))
            url = self.url_bv + bv
        else :
            url = self.url_bv+av_or_bv
        if not proxy_ok:
            requ = requests.get(url,headers=headers)
            video_data = requ.text
            if requ.text == self.error_msg_1 or requ.text == self.error_msg_2 :
                print("BV号或AV号无效")
            else :
                return video_data 
        elif proxy_ok :
            proxy_info = random.choice(list(proxy_ok.items()))
            proxies = {"https":"{0}:{1}".format(proxy_info[0],proxy_info[1])}
            requ = requests.get(url,headers=headers,proxies=proxies)
            video_data = requ.text
            if requ.text == self.error_msg_1 or requ.text == self.error_msg_2 :
                print("BV号或AV号无效")
            else :
                return video_data


    # def load_get_video_info(self,video_info) :
    #     # data_t = json.dumps(video_info,indent=4,separators=(",",":"),sort_keys=True).encode().decode('unicode-escape')
    #     global video_data
    #     video_data = json.loads(video_info)
    #     return video_data 

    def Parse_data(self,dict_name):
        # global show_data
        show_data = {}
        dict_2 = Split_dictionary(dict_name,"owner")
        dict_3 = Split_dictionary(dict_name,"stat")
        show_data["BV号"] = dict_name["bvid"]
        show_data["AV号"] = dict_name["aid"]
        show_data["标题"] = dict_name["title"]
        show_data["分类"] = dict_name["tname"]
        show_data["UP主"] = dict_2["name"]
        show_data["UP主头像"] = dict_2["face"]
        show_data["播放量"] = dict_3["view"]
        show_data["点赞"] = dict_3["like"] 
        show_data["回复"] = dict_3["reply"]
        show_data["收藏"] = dict_3["favorite"]
        show_data["投币数"] = dict_3["coin"]
        show_data["分享"] = dict_3["share"]
        show_data["频道"] = dict_name["dynamic"]
        return show_data
def Split_dictionary(dict_name,dict_key="data") :
    dict_split = {}
    if str(type(dict_name)) == "<class 'str'>" :
        dict_name_ = json.loads(dict_name)
        dict_use = dict_name_[dict_key]
    elif str(type(dict_name)) == "<class 'dict'>" :
        dict_use = dict_name[dict_key]
    for x in dict_use :    
        dict_split[x] = dict_use[x]
    return dict_split



bilibili = video_info()
print(bilibili.Parse_data(Split_dictionary(bilibili.get_video_info("av170001"))))