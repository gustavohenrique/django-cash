import os, sys
#sys.path.append('/home/gu/www/django')
sys.path.append('/home/gu/www/django/Django_Cash')
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

