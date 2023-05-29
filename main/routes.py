from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .psycho_tests import about_tests


class TestsApi(APIView):

    def get(self, request, *args, **kwargs):
        return Response(list(about_tests.keys()), status=status.HTTP_200_OK)
