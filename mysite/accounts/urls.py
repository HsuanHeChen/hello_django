from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^login/$', account_login, name='login'),
    url(r'^logout$', account_logout, name='logout'),
]
