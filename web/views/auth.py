from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from rbac import models
from utils.response import BaseResponse

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
            else:
                role = obj.roles.all()  # 查询当前用户的所有角色
                permissions_list = []  # 定义空列表

                for i in role:  # 循环角色
                    per = i.permissions.all()  # 查看当前用户所有角色的所有权限
                    # print(i.permissions.all())
                    for j in per:
                        # print(j.url)
                        # 将所有授权的url添加到列表中
                        permissions_list.append(j.url)

                # print(permissions_list)
                response.code = 1000

                # 增加session
                request.session['user'] = obj.name
                request.session['user_id'] = obj.id
                # url去重,因为多个角色,url会重复
                request.session['url'] = list(set(permissions_list))


        except Exception as e:
            response.code = 10005
            response.error = '操作异常'

        # print(response.dict)
        return Response(response.dict)
