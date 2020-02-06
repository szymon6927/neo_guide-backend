"""
Django settings for neo_guide project.

Generated by 'django-admin startproject' using Django 2.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import logging

import environ

logger = logging.getLogger(__name__)


env = environ.Env()

# Build paths inside the project like this: BASE_DIR('dir_name')
BASE_DIR = environ.Path(__file__) - 2


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', default=False)

ALLOWED_HOSTS = env('ALLOWED_HOSTS', default=[])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django_celery_beat',
    'rest_framework',
    'drf_yasg',
    'corsheaders',
    'storages',
    'django_filters',
    'neo_guide.users',
    'neo_guide.core',
    'neo_guide.psalms',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        },
    }
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {'default': env.db('DATABASE_URL')}

DATABASES['default']['CONN_MAX_AGE'] = 600

# Caches
# https://github.com/niwinz/django-redis

if 'CACHE_LOCATION' in env:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': env('CACHE_LOCATION'),
            'OPTIONS': {'CLIENT_CLASS': 'django_redis.client.DefaultClient'},
        }
    }


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers

AUTH_USER_MODEL = 'users.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR('staticfiles')

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR('media')

ADMIN_URL = env('ADMIN_URL', default='admin/')


# other django settings

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Corsheaders

CORS_ORIGIN_ALLOW_ALL = DEBUG

if not CORS_ORIGIN_ALLOW_ALL:
    CORS_ORIGIN_WHITELIST = env('CORS_ORIGIN_WHITELIST', default=[])


# Django Rest Framework

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
    ),
    'PAGE_SIZE': 10,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}


# AWS settings

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', default='')

AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', default='')

if 'AWS_STORAGE_BUCKET_NAME' in env:
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME', default='eu-central-1')
    AWS_LOCATION = env('AWS_LOCATION', default='staticfiles')
    AWS_LOCATION_MEDIA = env('AWS_LOCATION_MEDIA', default='mediafiles')
    AWS_S3_CUSTOM_DOMAIN = env(
        'CUSTOM_S3_BUCKET_REGIONAL_DOMAIN', default=f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'
    )
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    AWS_DEFAULT_ACL = 'public-read'
    # AWS_DEFAULT_ACL = None

    STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    DEFAULT_FILE_STORAGE = 'core.storage_backends.MediaStorage'
    MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION_MEDIA)


# Rollbar settings

ROLLBAR_ENVIRONMENT_PRODUCTION = 'production'
ROLLBAR_ENVIRONMENT_STAGING = 'staging'
ROLLBAR_ENVIRONMENT_OTHER = 'other'
ROLLBAR_ENVIRONMENT_OPTIONS = (ROLLBAR_ENVIRONMENT_PRODUCTION, ROLLBAR_ENVIRONMENT_STAGING, ROLLBAR_ENVIRONMENT_OTHER)

# Rollbar environment defaults to ROLLBAR_ENVIRONMENT_OTHER,
# which means that it will not report any errors, ex. during local development
rollbar_environment_value = env('ROLLBAR_ENVIRONMENT', default=ROLLBAR_ENVIRONMENT_OTHER)
if rollbar_environment_value not in ROLLBAR_ENVIRONMENT_OPTIONS:
    raise ValueError(
        f'Invalid value of ROLLBAR_ENVIRONMENT - "{rollbar_environment_value}". '
        f'Available values are: {", ".join(ROLLBAR_ENVIRONMENT_OPTIONS)}'
    )
elif rollbar_environment_value != ROLLBAR_ENVIRONMENT_OTHER:
    rollbar_access_token = env('ROLLBAR_ACCESS_TOKEN')
    if rollbar_access_token == '':
        raise ValueError('Rollbar access token cannot be an empty string')
    ROLLBAR = {
        'access_token': rollbar_access_token,
        'environment': rollbar_environment_value,
        'branch': env('ROLLBAR_BRANCH', default='master'),
        'root': BASE_DIR,
    }
else:
    logger.warning(
        f'Skipping Rollbar configuration, because ROLLBAR_ENVIRONMENT was set to "{rollbar_environment_value}"'
    )


# Celery

# CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='redis://redis:6379/1')
# CELERY_TASK_DEFAULT_QUEUE = env('CELERY_TASK_DEFAULT_QUEUE', default='default_queue')
# CELERY_BROKER_TRANSPORT_OPTIONS = {'region': env('AWS_REGION', default='eu-central-1')}
# CELERY_IGNORE_RESULT = True
# CELERY_RESULT_PERSISTENT = False


# APP
MAX_IMAGE_UPLOAD_SIZE = 3 * 1024 * 1024
MAX_AUDIO_UPLOAD_SIZE = 10 * 1024 * 1024
