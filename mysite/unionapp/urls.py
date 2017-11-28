from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.UnionList.as_view(), name='union_list'),
]