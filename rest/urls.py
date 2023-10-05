from django.urls import path
from . import views


urlpatterns = [
    path('tests', views.TestsApi.as_view(), name='tests_api'),
    path('telegramid/<int:telegram_id>', views.TelegramIDApi.as_view(), name='telegram_id_api'),
    path('passtest/<int:telegram_id>/<test_name>', views.PassTestApi.as_view(), name='pass_test_api'),
    path('stats/<int:telegram_id>/<test_name>', views.GetStatsApi.as_view(), name='get_stats_api'),

    path('telegramid/all_ids', views.TelAllTgIds.as_view(), name='all_ids'),
    path('telegramid/who_doesnt_pass/<test_name>/<int:days>', views.WhoDoesntPassTest.as_view(),
         name='who_doesnt_pass_the_test'),
]
