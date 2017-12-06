from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^ecapp24/$', ecapp24, name='ecapp24'),
    url(r'^996930e44ffd5292014e1460f72517f2355e1fa114f1ab5268/?$', PageWebHookView.as_view()),
    url(r'^lottery/$', TaiwanLotteryView.as_view(), name='lottery'),
]
