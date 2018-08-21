from django.shortcuts import render, redirect,HttpResponse
from rbac import models
from django.conf import settings


def login(request):
    """
    用户登陆
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request,'login.html')

    # 1. 获取提交的用户名和密码
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')

    # 2. 检验用户是否合法
    obj = models.UserInfo.objects.filter(name=user,password=pwd).first()
    if not obj:
        return render(request, 'login.html',{'msg':'用户名或密码错误'})

    # 3. 获取用户信息和权限信息写入session
    permission_list = obj.roles.filter(permissions__url__isnull=False).values('permissions__url').distinct()
    request.session['user_info'] = {'id':obj.id,'name':obj.name}
    request.session[settings.PERMISSION_SESSION_KEY] = list(permission_list)

    return redirect('/customer/list/')
