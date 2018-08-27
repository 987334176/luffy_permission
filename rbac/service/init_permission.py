from django.conf import settings


def init_permission(request, user):
    """
    权限和菜单信息初始化，以后使用时，需要在登陆成功后调用该方法将权限和菜单信息放入session
    :param request:
    :param user:
    :return:
    """

    # 3. 获取用户信息和权限信息写入session
    permission_queryset = user.roles.filter(permissions__url__isnull=False).values('permissions__id',
                                                                                   'permissions__url',
                                                                                   'permissions__title',
                                                                                   'permissions__name',
                                                                                   'permissions__parent_id',
                                                                                   'permissions__parent__name',
                                                                                   'permissions__menu_id',
                                                                                   'permissions__menu__title',
                                                                                   'permissions__menu__icon',
                                                                                   ).distinct()


    menu_dict = {}  # 菜单字典,它是能成为菜单的权限,用于做菜单显示
    permission_dict = {}  #  权限列表,所有权限,用于做权限校验

    for row in permission_queryset:
        # 以url别名为key
        permission_dict[row['permissions__name']] = {
            # 权限id
            'id': row['permissions__id'],
            # url
            'url': row['permissions__url'],
            'title': row['permissions__title'],
            # 权限父id
            'pid': row['permissions__parent_id'],
            # 父id的name
            'pname': row['permissions__parent__name'],
        }

        # 获取菜单id
        menu_id = row.get('permissions__menu_id')
        # 如果菜单id为空,跳过此次循环
        if not menu_id:
            continue

        # 判断菜单id不在字典里面时,避免一级菜单重复
        if menu_id not in menu_dict:
            # 以菜单id为key
            menu_dict[menu_id] = {
                # value部分就是title,用来展示一级菜单
                'title': row['permissions__menu__title'],
                # 一级菜单的图标
                'icon': row['permissions__menu__icon'],
                # 二级菜单
                'children': [
                    # 二级菜单标题和url。注意:一级标题是不能点击的,所以它没有url
                    # 二级菜单是可以点击的,但是它没有图标
                    {'id':row['permissions__id'],'title': row['permissions__title'], 'url': row['permissions__url']}
                ]
            }
        else:
            # 如果一级菜单还有二级菜单,就继续添加
            menu_dict[menu_id]['children'].append({'id':row['permissions__id'],'title': row['permissions__title'], 'url': row['permissions__url']})


    request.session[settings.PERMISSION_SESSION_KEY] = permission_dict
    request.session[settings.MENU_SESSION_KEY] = menu_dict
