from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^$', UnionList.as_view(), name='union_list'),
    url(r'^(?P<pk>\d+)/$', UnionDetailView.as_view(), name='union_detial'),
    url(r'^new/$', UnionCreateView.as_view()),
]