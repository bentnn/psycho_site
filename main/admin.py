from django.contrib import admin
from . import models
from inspect import getmembers, isclass
from django.conf import settings
import re
from .psycho_tests import about_tests

if settings.DEBUG:
    for test in about_tests.values():
        admin.site.register(test['model'])
    # for name, cls in getmembers(models, isclass):
    #     if re.match(r'Test\d+', name) is not None:
    #         admin.site.register(cls)
