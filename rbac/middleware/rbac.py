from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.shortcuts import redirect,HttpResponse
import re

class RbacMiddleware(MiddlewareMixin):
    """
    权限控制的中间件
    """

    def process_request(self, request):
        """
        权限控制
        :param request:
        :return:
        """
        # 1. 获取当前请求URL
        current_url = request.path_info
        # print(current_url)

        # 1.5 白名单处理
        for reg in settings.VALID_URL:
            if re.match(reg,current_url):
                return None

        # 2. 获取当前用户session中所有的权限
        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        if not permission_dict:
            return redirect('/login/')

        # 3. 路径导航列表,首页是必须有的
        request.breadcrumb_list = [
            {'title': '首页', 'url': '/'},
        ]

        # 4. 进行权限校验
        flag = False
        for item in permission_dict.values():
            id = item.get('id')  # url的id
            pid = item.get('pid')  # url的pid
            pname = item.get('pname')  # url的别名

            # 获取url
            reg = "^%s$" % item.get('url')
            if re.match(reg, current_url):
                flag = True
                if pid:  # 如果是有pid的url,比如添加客户
                    # 当前菜单id取pid
                    request.current_menu_id = pid
                    # 追加url菜单
                    request.breadcrumb_list.extend([
                        # 二级菜单和二级菜单下的非菜单url
                        {'title': permission_dict[pname]['title'], 'url': permission_dict[pname]['url']},
                        {'title': item['title'], 'url': item['url']},
                    ])
                else:
                    # 否则就是二级菜单。因为一级菜单无法点击,这里只能是二级
                    request.current_menu_id = id
                    request.breadcrumb_list.extend([
                        # 二级菜单
                        {'title': item['title'], 'url': item['url']},
                    ])

                break
        if not flag:
            return HttpResponse('无权访问')