# -*- coding: utf-8 -*-
import os
PROJECT_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Gustavo Henrique', 'gustavo@gustavohenrique.net'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(PROJECT_ROOT_PATH, 'money.db')
DATABASE_USER = 'usuario'
DATABASE_PASSWORD = 'senha'
DATABASE_HOST = ''
DATABASE_PORT = ''

TIME_ZONE = 'America/Sao_Paulo'
LANGUAGE_CODE = 'pt-br'
SITE_ID = 1
USE_I18N = True
MEDIA_ROOT = os.path.join(PROJECT_ROOT_PATH, 'media')
MEDIA_URL = '/media'
ADMIN_MEDIA_PREFIX = '/media/admin/'
SECRET_KEY = 's6bpekeq7yha#lg&=09ke_*66q_g7_upi+w-$$n%t4+gmnaz2l'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT_PATH, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'money',
    'tagging',
)

LOGIN_URL = '/auth/login/'
LOGOUT_URL = '/auth/logout/'
LOGIN_REDIRECT_URL = '/money/'
DATE_FORMAT = '%d/%m/%Y'
DATETIME_FORMAT = 'd/m/Y - H:i:s'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
FORCE_LOWERCASE_TAGS = True
LINHAS_POR_GRID = 31
