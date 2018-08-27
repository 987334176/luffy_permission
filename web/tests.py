from django.test import TestCase

# Create your tests here.
import os

if __name__ == "__main__":
    # 设置django环境
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "luffy_permission.settings")
    import django
    django.setup()

    from rbac import models

    # 固定用户名和密码
    user = 'xiao'
    pwd = '123'
    # 查询表，用户名和密码是否匹配
    obj = models.UserInfo.objects.filter(name=user, password=pwd).first()
    permission_queryset = obj.roles.filter(permissions__url__isnull=False).values('permissions__url',
                                                                                   'permissions__title',
                                                                                   'permissions__menu_id',
                                                                                   'permissions__menu__title',
                                                                                   'permissions__menu__icon',
                                                                                   ).distinct()
    print(permission_queryset)

'''
信息管理
    账单列表(可做菜单的权限)
        添加账单
        删除账单
        编辑账单
客户管理
    客户列表(可做菜单的权限)

menu_dict = {
    1:{
        'title':'信息管理',
        'icon':'fa-coffee',
        'class':''
        'children':{
            {'id':1,'title':'客户列表','url':'/customer/list/','class':'active'}
        }
    }
}

permission_dict = {
    'customer_list':{'id': 1, 'url': '/customer/list/', 'title':'客户列表','pid': None},
    'customer_add':{'id': 2, 'url': '/customer/add/', 'title':'添加客户','pid': 1},
    'customer_edit':{'id': 3, 'url': '/customer/edit/', 'title':'编辑客户', 'pid': 1},
}
if 'customer_add' in permission_dict:
    print('有权限')
else:
    print('无权限')
    
1. 如何实现的权限系统？
    粒度控制到按钮级别的权限控制
        - 用户登陆成功之后，将权限和菜单信息放入session
        - 每次请求时，在中间件中做权限校验
        - inclusion_tag实现的动态菜单
2. 如何实现控制到按钮的呢？
    用户登陆时，用户所拥有的权限 别名==django 路由name 构造成一个字典；
    在页面中写了一个 django模板的filter来进行判断是否显示；

3. 为什么要在中间件中做校验呢？
    所有请求在到达视图函数之前，必须经过中间件，所以在中间件中对请求做处理比较简单；

4. 模板中的特殊方法：inclusion_tag、simpletag、filter

5. 权限中使用了几张表？	
    六张，必须要说出来

6. 表中的字段？（背表）

7. 写流程（思维导读）

8. 如何实现粒度到数据行？
    答：添加一条更细粒度的表，做条件用；
    
9. 修改权限之后，如想应用最新权限
    - 我们：需要重新登陆。
    - 不用重新登陆，如何完成？更新涉及的所有用户的session信息
    
10. 最重要 *****
    - 了解权限系统的流程和实现（一行一行过，根据表结构自己写）    不要抄
    - 权限组件的应用
    
流程是不变的

中间件-->白名单
权限初始化，数据库有6张表。
菜单，权限，角色，3个关系表
表里面有哪些字段
最重要的权限表
id,name,title,menu
name 用来做反向生成
有的公司叫code

pid  作用：让添加客户端，默认展示相关的子菜单
meum_id：作用：因为要做二级菜单

获取相关的权限信息。session放了2个东西。菜单和权限信息
它都是字典
permission_dict 以别名做为key
menu_dict 一级菜单id作为Key

中间件，请求信息做校验
成功之后，pid对应的菜单，默认展开
还是一个就是导航条，自动生成
最重要的功能，权限验证
还有一个白名单

requetst多了2个值,current_menu_id,breadcrumb_list
在模板里面做了一些事情，动态生成菜单，粒度控制在按钮级别
公共应用都是inclusion_tag和filter
只有filter作为if后面的条件


'''