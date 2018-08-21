from django.shortcuts import render, redirect, HttpResponse
from rbac import models
from rbac.service.init_permission import init_permission
from django.conf import settings


def login(request):
    """
    用户登陆
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'login.html')

    # 1. 获取提交的用户名和密码
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')

    # 2. 检验用户是否合法
    obj = models.UserInfo.objects.filter(name=user, password=pwd).first()
    if not obj:
        return render(request, 'login.html', {'msg': '用户名或密码错误'})

    # 写入session
    request.session['user_info'] = {'id': obj.id, 'name': obj.name}
    # 初始化权限,并写入session
    init_permission(request, obj)

    return redirect('/customer/list/')

