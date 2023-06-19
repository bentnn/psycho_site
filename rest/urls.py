from django.urls import path
from . import views


urlpatterns = [
    path('tests', views.TestsApi.as_view(), name='tests_api'),
    path('telegramid/<int:telegram_id>', views.TelegramIDApi.as_view(), name='telegram_id_api'),
]
