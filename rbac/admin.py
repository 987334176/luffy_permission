from django.contrib import admin

# Register your models here.
from rbac import models

admin.site.register(models.Permission)
admin.site.register(models.Role)
admin.site.register(models.UserInfo)