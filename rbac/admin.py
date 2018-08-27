from django.contrib import admin
from rbac import models

admin.site.register(models.Menu)

class PermissionAdmin(admin.ModelAdmin):
    list_display = ['title','url','parent','name']  # 显示的字段
    list_editable = ['url','parent','name']  # 允许编辑

admin.site.register(models.Permission,PermissionAdmin)


admin.site.register(models.Role)
admin.site.register(models.UserInfo)