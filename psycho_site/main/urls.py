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
    path('test1', views.test_first, name='test_first'),
    path('test2', views.test_second, name='test_second'),
    path('test3', views.test_third, name='test_third'),
    path('test4', views.test_fourth, name='test_fourth'),
    path('test5', views.test_fifth, name='test_fifth'),
    path('staffroom', views.staffroom, name='staffroom'),
]