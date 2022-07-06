from django.contrib import admin
from . import models
from inspect import getmembers, isclass
from django.conf import settings
import re

if settings.DEBUG:
    for name, cls in getmembers(models, isclass):
        if re.match(r'Test\d+', name) is not None:
            admin.site.register(cls)
