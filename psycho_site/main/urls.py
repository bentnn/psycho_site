from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login_view, name='login'),
    path('signout', views.signout_view, name='signout'),
    path('account', views.account, name='account'),
    path('statistics', views.statistics, name='statistics'),
    path('account/change_password', views.change_password, name='change_password'),
    path('test_first', views.test_first, name='test_first'),
]