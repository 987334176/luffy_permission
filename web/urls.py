from django.conf.urls import url
from web.views import customer
from web.views import payment
from web.views import account

urlpatterns = [

    url(r'^login/$', account.login),


    url(r'^customer/list/$', customer.customer_list),
    url(r'^customer/add/$', customer.customer_add),
    url(r'^customer/edit/(?P<cid>\d+)/$', customer.customer_edit),
    url(r'^customer/del/(?P<cid>\d+)/$', customer.customer_del),
    url(r'^customer/import/$', customer.customer_import),
    url(r'^customer/tpl/$', customer.customer_tpl),

    url(r'^payment/list/$', payment.payment_list),
    url(r'^payment/add/$', payment.payment_add),
    url(r'^payment/edit/(?P<pid>\d+)/$', payment.payment_edit),
    url(r'^payment/del/(?P<pid>\d+)/$', payment.payment_del),
]
