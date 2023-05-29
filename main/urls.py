from django.urls import path
from .psycho_tests import about_tests
from . import views
from . import routes


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
    path('staffroom', views.staffroom, name='staffroom'),
    path('download_emails', views.download_emails, name='download_emails'),

    # api
    path('api', routes.TestsApi.as_view()),

    # tests pages
    *[path(name, getattr(views, name), name=name) for name in about_tests.keys()]
]
