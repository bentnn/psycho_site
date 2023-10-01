from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from main.psycho_tests import about_tests
from main import test_counters
from rest.models import UserTelegramID
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAdminUser
from main.models import BaseTestModel
import logging

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


class PassTestApi(BaseTelegramRest):

    def post(self, request: Request, telegram_id, test_name, *args, **kwargs):
        user_telegram = get_user_telegram(telegram_id=telegram_id)
        if not user_telegram:
            return Response('Unknown user', status=404)
        if test_name not in about_tests:
            return Response(f'Unknown test {test_name}', status=404)
        data = request.data
        print(data)
        msg = getattr(test_counters, f'count_{test_name}')({str(n): i for n, i in enumerate(data, start=1)},
                                                           user=user_telegram.user, via_telegram=True)
        return Response(msg, status=200)


class GetStatsApi(BaseTelegramRest):

    def get(self, request: Request, telegram_id, test_name, *args, **kwargs):

        def create_test_stats_resp(name_of_test) -> dict:

            def get_about_test_info(test_object, message: str = None):
                return {
                    'message': message,
                    'result': {test_object._meta.get_field(j).verbose_name: getattr(test_object, j) for j in about_tests[name_of_test]['model'].resulting_fields}
                }

            test_stats = about_tests[name_of_test]['model'].objects.filter(user=user_telegram.user).order_by('-id')[:20]
            # test_stats = about_tests[name_of_test]['model'].objects.filter(user=user_telegram.user).order_by('-id')[:20][::-1]
            # verbose_name
            res = {f'{i.date} {i.time}': get_about_test_info(i, message=i.message) for i in test_stats[:5]}
            res.update((f'{i.date} {i.time}', get_about_test_info(i, message=None)) for i in test_stats[5:])

            return {about_tests[name_of_test]['name']: res}
            # return {about_tests[name_of_test]['name']: {f'{i.date} {i.time}': i.message for i in test_stats}}

        user_telegram = get_user_telegram(telegram_id=telegram_id)
        if not user_telegram:
            return Response('Unknown user', status=404)
        if test_name == 'all':
            res = {}
            for i in about_tests:
                test_res = create_test_stats_resp(i)
                # проверка, что результаты были найдены
                if test_res[about_tests[i]['name']]:
                    res.update(test_res)
            return Response(res, status=200)
        elif test_name in about_tests:
            return Response(create_test_stats_resp(test_name), status=200)
        else:
            return Response(f'Unknown test {test_name}', status=404)


class TelAllTgIds(BaseTelegramRest):

    def get(self, request: Request, *args, **kwargs):
        all_ids = UserTelegramID.objects.all()
        logging.info('Len of all tg ids: ' + str(len(all_ids)))
        return Response([i.telegram_id for i in all_ids], status=200)


class WhoDoesntPassTest(BaseTelegramRest):
    def get(self, request: Request, test_name: str, days: int, *args, **kwargs):
        if test_name not in about_tests:
            return Response(f'Unknown test {test_name}', status=404)
        all_ids = UserTelegramID.objects.all()
        about_tests[test_name]['model'].objects.filter().all()