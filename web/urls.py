from django.conf.urls import url
from web.views import customer,payment,auth,login

urlpatterns = [
    # 客户管理
    url(r'^customer/list/$', customer.customer_list),
    url(r'^customer/add/$', customer.customer_add),
    url(r'^customer/edit/(?P<cid>\d+)/$', customer.customer_edit),
    url(r'^customer/del/(?P<cid>\d+)/$', customer.customer_del),
    url(r'^customer/import/$', customer.customer_import),
    url(r'^customer/tpl/$', customer.customer_tpl),
    # 账单管理
    url(r'^payment/list/$', payment.payment_list),
    url(r'^payment/add/$', payment.payment_add),
    url(r'^payment/edit/(?P<pid>\d+)/$', payment.payment_edit),
    url(r'^payment/del/(?P<pid>\d+)/$', payment.payment_del),
    # 登录相关
    url(r'^$', login.login),  # 前端
    url(r'^login/$', login.login),
    url(r'^auth/$', auth.AuthView.as_view({'post': 'login'})),  # 认证api
]
