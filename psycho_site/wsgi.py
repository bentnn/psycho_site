# -*- coding: utf-8 -*-

import os
import sys
import platform

#путь к проекту
sys.path.insert(0, '/home/c/cw97231/psycho/public_html/psycho_site')
#путь к фреймворку
sys.path.insert(0, '/home/c/cw97231/psycho/public_html/psycho_site/psycho_site')
#путь к виртуальному окружению
sys.path.insert(0, '/home/c/cw97231/psycho/myenv/lib/python{0}/site-packages'.format(platform.python_version()[0:3]))
os.environ["DJANGO_SETTINGS_MODULE"] = "psycho_site.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()