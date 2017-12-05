from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^ecapp24/$', ecapp24, name='ecapp24'),
]
