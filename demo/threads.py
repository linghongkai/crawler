import json
import socket
import threading
import time

import requests
from lxml import etree

from demo.models import Info, User

URL = 'https://info.18art.art/html/infor/infor.html?v=1680598308225'
HEADER = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/111.0.0.0 Mobile Safari/537.36 Edg/111.0.1661.62 ',
    'referer': 'https://info.18art.art/',
    'accept-encoding': 'gzip, deflate, br'
}


def send(url, message):
    group_list = User.objects.all()
    for group in group_list:
        print(group)
        if group.category == 'group':
            send_group_msg(group.number, url, message)


def send_group_msg(group_id, url, message):
    # url = 'http://localhost:5700/send_group_msg'
    #
    # # 请求头
    # headers = {
    #     'Content-Type': 'application/json'
    # }
    # data = {
    #     'group_id': group_id,
    #     'message': message
    # }
    # response = requests.post(url=url, headers=headers, data=data)
    global payload
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ip = '127.0.0.1'
    client.connect((ip, 5700))

    msg_type = 'group'  # 回复类型（群聊/私聊）
    number = group_id  # 回复账号（群号/好友号）
    msg = message+'网址：'+url  # 要回复的消息

    # 将字符中的特殊字符进行url编码
    msg = msg.replace(" ", "%20")
    msg = msg.replace("\n", "%0a")

    if msg_type == 'group':
        payload = "GET /send_group_msg?group_id=" + str(
            number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"
    # elif msg_type == 'private':
    #     payload = "GET /send_private_msg?user_id=" + str(
    #         number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"
    print("发送" + payload)
    client.send(payload.encode("utf-8"))
    client.close()


def spider():
    response = requests.get(url=URL, headers=HEADER)
    response.encoding = "utf-8"
    page_text = response.text
    tree = etree.HTML(page_text)
    script_json = tree.xpath('/html/head/script[3]/text()')
    script_str = str(script_json)
    script_str = script_str.replace(';', '')
    script_str = script_str.replace(' ', '')
    script_str = script_str.replace("']", '')
    script_str = script_str.replace('\\n', '')
    var = script_str.split('window.__injectJson=')[1]
    s_json = json.loads(var)
    res_list = s_json['noticeList']
    for i in range(5):
        for res in res_list:
            if len(res['list']) <= i:
                continue
            title = res['list'][i]['title']
            url = res['list'][i]['url']
            print(title, url)
            # 用filter()方法查找匹配的Info对象，如果不存在则创建一个新的
            info_list = Info.objects.filter(title=title)
            if not info_list:
                oldTime = res['list'][i]['time']/1000
                nowTime = time.time()
                if nowTime-oldTime > 60*5:
                    continue
                send(url, title)
                Info.objects.create(title=title, url=url)


class SpiderThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            spider()
            time.sleep(30)
