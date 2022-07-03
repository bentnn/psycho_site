from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login_view, name='login'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('check_in', views.check_in_view, name='check_in'),
    path('signout', views.signout_view, name='signout'),
    path('account', views.account, name='account'),
    path('change_info', views.change_info, name='change_info'),
    path('statistics', views.statistics, name='statistics'),
    path('account/change_password', views.change_password, name='change_password'),
    path('tests', views.tests, name='tests'),
    path('test1', views.test1, name='test1'),
    path('test2', views.test2, name='test2'),
    path('test3', views.test3, name='test3'),
    path('test4', views.test4, name='test4'),
    path('test5', views.test5, name='test5'),
    path('test6', views.test6, name='test6'),
    path('test7', views.test7, name='test7'),
    path('test8', views.test8, name='test8'),
    path('test9', views.test9, name='test9'),
    path('staffroom', views.staffroom, name='staffroom'),
    path('download_emails', views.download_emails, name='download_emails'),
]
