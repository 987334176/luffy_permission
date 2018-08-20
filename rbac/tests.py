from django.test import TestCase

# Create your tests here.
import os

if __name__ == "__main__":
    # 设置django环境
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "luffy_permission.settings")
    import django
    django.setup()

    from rbac import models

    user = 'xiao'
    pwd = '123'

    obj = models.UserInfo.objects.filter(name=user, password=pwd).first()
    role = obj.roles.all()
    permissions_list = []

    for i in role:
        per = i.permissions.all()
        # print(i.permissions.all())
        for j in per:
            # print(j.url)
            permissions_list.append(j.url)

    print(permissions_list)


