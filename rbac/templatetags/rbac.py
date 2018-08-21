from django.template import Library
from django.conf import settings
import re
register = Library()


@register.inclusion_tag('rbac/menu.html')
def menu(request):
    """
    生成菜单
    :param request:
    :return:
    """

    # 获取session中的菜单列表
    menu_list = request.session.get(settings.MENU_SESSION_KEY)

    for item in menu_list:
        # 每一个url增加^$,比如/customer/list/变成^/customer/list/$
        reg = "^%s$" % item['url']
        if re.match(reg,request.path_info):  # 判断当前路径是否匹配
            # 增加一个样式,class为action。表示选中状态
            item['class'] = 'active'

    return {'menu_list':menu_list}  # 变量传给模板