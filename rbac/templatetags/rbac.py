from django.template import Library
from django.conf import settings
import re
from collections import OrderedDict

register = Library()


@register.inclusion_tag('rbac/menu.html')
def menu(request):
    """
    生成菜单
    :param request:
    :return:
    """

    # 获取session中的菜单列表
    menu_dict = request.session.get(settings.MENU_SESSION_KEY)
    ordered_dict = OrderedDict()  # 实例化

    for key in sorted(menu_dict):
        # 对字典的key做排序,并添加到有序字典对象中
        ordered_dict[key] = menu_dict[key]
        # 默认所有的一级菜单隐藏
        menu_dict[key]['class'] = 'hide'
        # 循环二级菜单
        for node in menu_dict[key]['children']:
            # 正则表达式,为url添加^和$
            reg = "^%s$" %node['url']
            # 判断当前url的菜单id等于二级菜单id
            # 因为权限表的url能成为菜单的都是二级菜单
            if request.current_menu_id == node['id']:
                # 增加选中样式,给前端展示
                node['class'] = 'active'
                # 点击二级菜单时,让当前所在的一级菜单展示
                # 因为上面，把所有的一级菜单给隐藏了.这里设置为空,表示显示
                menu_dict[key]['class'] = ''

    return {'menu_dict':ordered_dict}  # 变量传给模板


@register.inclusion_tag('rbac/breadcrumb.html')
def breadcrumb(request):
    """
    路径导航
    :param request:
    :return:
    """
    return {'breadcrumb_list':request.breadcrumb_list}

@register.filter
def has_permission(request,name):
    """
    权限判断
    :param request:
    :param name: url别名
    :return: 如果别名在权限字典里,返回True。否则返回None
    """
    permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
    if name in permission_dict:
        return True