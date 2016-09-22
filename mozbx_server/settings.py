"""
Django settings for mozbx_server project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOG_FILE = "/opt/Code/mozbx_server/get_web/zbx_in_db.log"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_g2nyj!nzyh9esskwvln38n3bk+fw)(hvt+4&s#vy0+gng1mzq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.staticfiles',
    'django_crontab',
    'get_web',
    'SALT',
    'ASSETS',
    'ZABBIX',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mozbx_server.urls'

TEMPLATE_DIRS = (
    '/opt/Code/mozbx_server/templates',
)

STATICFILES_DIRS = (
    '/opt/Code/mozbx_server/static',
)

WSGI_APPLICATION = 'mozbx_server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "mozbx_server",
        'USER': "mozbx",
        'PASSWORD': "VsfuTiAB3bfzgebbFf9d",
        'HOST': "127.0.0.1",
        'PORT': 3306,
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
LOGIN_URL = '/login/'

CRONJOBS = [
    ('*/5 * * * *', 'get_web.getinfo.war_in_db', '>> ' + LOG_FILE),
    ('*/10 * * * *', 'get_web.getinfo.srv_in_db', '>> ' + LOG_FILE),
    ('*/5 * * * *', 'get_web.getinfo.uptime_in_db', '>> ' + LOG_FILE),
    ('*/5 * * * *', 'get_web.getinfo.ora_in_db', '>> ' + LOG_FILE),
    ('2 0 * * *', 'get_web.getinfo.cre_free_temp', '>> ' + LOG_FILE),
    ('5 1 * * *', 'get_web.getinfo.memt_in_db', '>> ' + LOG_FILE),
]
