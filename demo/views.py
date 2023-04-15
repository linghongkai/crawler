import json

import requests
from django.shortcuts import redirect
from django.shortcuts import render

from demo.models import User


# Create your views here.
def index(request):
    user = User.objects.all()
    context = list(user)
    id_list = []
    for u in context:
        id_list.append(u.number)
    print(id_list)
    context = []
    # getUser(context, id_list)
    getGroup(context, id_list)
    # context = [
    #     {'name': 'lhk', 'number': '2040', 'category': 'private', 'isSelected': False},
    #     {'name': 'lhk', 'number': '20410', 'category': 'pr1ivate', 'isSelected': False}
    # ]
    return render(request, 'demo/index.html', {'user_list': context})


def subData(request):
    userList = request.POST.getlist('userList')
    # for user in userList:
    #     print(eval(str))
    res_list = []
    for user in userList:
        user = eval(user)
        user['isSelected'] = True
        user_obj = User(**user)  # 创建 User 对象
        user_obj.id = user_obj.number
        res_list.append(user_obj)

    User.objects.bulk_create(res_list)
    return redirect('demos:success')


def deleteData(request):
    userList = request.POST.getlist('userList')
    context = User.objects.all()
    for user in context:
        if user not in userList:
            User.objects.get(id=user.id).delete()
    return redirect('demos:success')


def success(request):
    return render(request, 'demo/success.html')


def drop(request):
    context = User.objects.all()
    return render(request, 'demo/drop.html', {'user_list': context})


def getUser(context, id_list):
    url = 'http://localhost:5700/get_friend_list'

    # 请求头
    headers = {
        'Content-Type': 'application/json'
    }

    # 发送GET请求
    response = requests.get(url, headers=headers)

    # 解析JSON数据
    data = json.loads(response.text)
    friend_list = data['data']
    for friend in friend_list:
        if str(friend['user_id']) not in id_list:
            context.append({
                'name': friend['nickname'],
                'number': friend['user_id'],
                'category': 'private',
                'isSelected': False
            })


def getGroup(context, id_list):
    url = 'http://localhost:5700/get_group_list'

    # 请求头
    headers = {
        'Content-Type': 'application/json'
    }

    # 发送GET请求
    response = requests.get(url, headers=headers)

    # 解析JSON数据
    data = json.loads(response.text)
    group_list = data['data']
    for group in group_list:
        if str(group['group_id']) not in id_list:
            context.append({
                'name': group['group_name'],
                'number': group['group_id'],
                'category': 'group',
                'isSelected': False
            })








