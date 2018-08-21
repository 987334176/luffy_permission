from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from rbac import models
from utils.response import BaseResponse
from django.conf import settings

class AuthView(ViewSetMixin,APIView):
    authentication_classes = []  # 空列表表示不认证

    def login(self,request,*args,**kwargs):
        """
        用户登陆认证
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = BaseResponse()  # 默认状态
        try:
            user = request.data.get('username')
            pwd = request.data.get('password')
            # print(user,pwd)
            # 验证用户和密码
            obj = models.UserInfo.objects.filter(name=user,password=pwd).first()
            if not obj:  # 判断查询结果
                response.code = 1002
                response.error = '用户名或密码错误'
                return Response(response.dict)

            # 过滤url为空的,使用distinct去重。因为用户有多个角色,存在url重复的情况
            permission_list = obj.roles.filter(permissions__url__isnull=False).values("permissions__url").distinct()

            response.code = 1000

            # 增加session
            request.session['user_info'] = {'id':obj.id,'name':obj.name}

            request.session[settings.PERMISSION_SESSION_KEY] = list(permission_list)


        except Exception as e:
            response.code = 10005
            response.error = '操作异常'

        # print(response.dict)
        return Response(response.dict)
