from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^$', UnionList.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', UnionDetail.as_view(), name='detial'),
    url(r'^(?P<pk>\d+)/edit$', UnionUpdate.as_view(), name='edit'),
    url(r'^new/$', UnionCreate.as_view(), name='new'),
]