from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect, HttpResponse
from luffy_permission import settings
import os

class AuthMD(MiddlewareMixin):  # 验证登录
    white_list = ['/','/login/','/auth/','/admin/' ]  # 白名单
    # black_list = ['/black/', ]  # 黑名单
    ret = {"status": 0, 'url': '', 'msg': ''}  # 默认状态

    def process_request(self, request):  # 请求之前
        request_url = request.path_info  # 获取请求路径
        # get_full_path()表示带参数的路径
        # print(request.path_info, request.get_full_path())

        # 判断请求路径不在白名单中
        if request_url not in self.white_list:
            import re
            # 获取用户session中的url列表
            per_url = request.session.get(settings.PERMISSION_SESSION_KEY)
            # print(per_url)
            if per_url:
                for i in per_url:  # 循环url列表
                    i = i.get('permissions__url')
                    print(i)
                    # 使用正则匹配。其中i为正则表达式,request_url.lstrip('/')表示去除左边的'/'
                    result = re.match(i, request_url.lstrip('/'))
                    # print(result)
                    if result:  # 判断匹配结果
                        print('授权通过',request_url)
                        return None  # return None表示可以继续走下面的流程
                    # else:
                    #     print('授权不通过',request_url)
                    #     # return redirect('/login/')


                # 错误页面提示
                self.ret['msg'] = "未授权,禁止访问!"
                self.ret['url'] = "/login/"
                path = os.path.join(settings.BASE_DIR, 'web/templates/error.html'),
                return render(request, path, self.ret)  # 渲染错误页面