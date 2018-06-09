import re
from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from user.models import UserModel, UserTicketModel
from utils.functions import get_ticket


def login(request):
    """
    登录
    :param request:
    :return:
    """

    if request.method == 'GET':

        return render(request, 'user/login.html')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('pwd')

        if UserModel.objects.filter(username=username).exists():
            user = UserModel.objects.filter(username=username).first()
            if check_password(password, user.password):
                ticket = get_ticket()
                out_time = datetime.now() + timedelta(days=7)
                response = HttpResponseRedirect(reverse('app:index'))
                response.set_cookie('ticket', ticket)
                UserTicketModel.objects.create(user_id=user.id, ticket=ticket, out_time=out_time)
                return response
            return render(request, 'user/login.html', {'msg': '用户名或密码错误'})
        return render(request, 'user/login.html', {'msg': '用户名或密码错误'})


def register(request):
    """
    注册
    :param request:
    :return:
    """

    if request.method == 'GET':

        return render(request, 'user/register.html')

    if request.method == 'POST':

        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        password1 = request.POST.get('cpwd')
        email = request.POST.get('email')

        # 验证用户信息
        reg1 = re.match(r'^\w{5,20}', username)
        reg2 = re.match(r'^\w{8,20}', password)
        if not reg1:
            return render(request, 'user/register.html', {'msg': '请输入5-20个字符的用户名'})
        if not reg2:
            return render(request, 'user/register.html', {'msg': '密码最少8位，最长20位'})
        if password != password1:
            return render(request, 'user/register.html', {'msg': '两次输入的密码不一致'})

        # 在数据库中记录用户信息
        UserModel.objects.create(username=username,
                                 password=make_password(password),
                                 email=email)
        # 用户信息储存后重定向到登录界面
        return HttpResponseRedirect(reverse('user:login'))


def logout(request):

    if request.method == 'GET':

        response = render(request, 'index/index.html')
        response.delete_cookie('ticket')

        return response
