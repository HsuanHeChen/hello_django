from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^new$', new_list, name='new_list'),
    url(r'^(?P<pk>\d+)/$', view_list, name='view_list'),
    url(r'^users/(?P<pk>\d+)/$', my_lists, name='my_lists'),
]
