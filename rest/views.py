from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from main.psycho_tests import about_tests
from rest.models import UserTelegramID
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAdminUser

short_about_test = {
    test_name: {
        'name': test_info['name'],
        'info': test_info['info'],
        'questions': test_info['questions'],
        'instruction': test_info['instruction'],
        'answers': test_info['answers'],
    }
    for test_name, test_info in about_tests.items()
}


class BaseTelegramRest(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser]


class TestsApi(BaseTelegramRest):

    def get(self, request, *args, **kwargs):
        return Response(short_about_test, status=status.HTTP_200_OK)


def get_user_telegram(**kwargs):
    try:
        return UserTelegramID.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return None


class TelegramIDApi(BaseTelegramRest):

    def get(self, request, telegram_id, *args, **kwargs):
        user_telegram = get_user_telegram(telegram_id=telegram_id)
        if user_telegram:
            return Response(
                {'username': user_telegram.user.username,
                 'first_name': user_telegram.user.first_name,
                 'last_name': user_telegram.user.last_name},
                status=200)
        else:
            return Response(status=404)

    def delete(self, request, telegram_id, *args, **kwargs):
        user_telegram = get_user_telegram(telegram_id=telegram_id)
        if user_telegram:
            user_telegram.delete()
            return Response(status=200)
        else:
            return Response(status=404)
