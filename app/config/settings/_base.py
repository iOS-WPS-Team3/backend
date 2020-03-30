"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import json
import os

import boto3

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

secret_name = 'WPSiOS'
region_name = 'ap-northeast-2'

session = boto3.session.Session(
    profile_name='WPSiOS',
    region_name=region_name
)

client = session.client(
    service_name='secretsmanager',
    region_name=region_name,
)

SECRETS_STRING = client.get_secret_value(SecretId='WPSiOS')['SecretString']
SECRETS = json.loads(SECRETS_STRING)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRETS['SECRET_KEY']

# S3
AWS_STORAGE_BUCKET_NAME = SECRETS['AWS_STORAGE_BUCKET_NAME']
AWS_S3_REGION_NAME = SECRETS['AWS_S3_REGION_NAME']
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'

# s3 static settings
STATIC_LOCATION = 'static'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
STATICFILES_STORAGE = 'config.storages.S3StaticStorage'

# s3 media settings
MEDIA_LOCATION = 'media'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/'
DEFAULT_FILE_STORAGE = 'config.storages.S3MediaStorage'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'members.User'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'drf_yasg',
    'corsheaders',
    'phonenumber_field',
    'rest_framework',
    'rest_framework.authtoken',
    'storages',

    'members.apps.MembersConfig',
    'kurly.apps.KurlyConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# DRF Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}

# drf-yasg
BASIC_DESCRIPTION = '''
<개발용>
**사용자 ID / 비밀번호** 쌍을 Header에 전달\n
HTTP Request의 Header `Authorization`에 
`Basic <"username:password" 문자열>`값을 전송\n
```
Authorization: Basic ZGVmYXVsdF9jb21wYW55QGxoeS5rcjpkbGdrc2R1ZA==
```
'''
TOKEN_DESCRIPTION = '''
### [DRF AuthToken](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)
인증정보를 사용해 [TokenAPI](#operation/api-token-auth_create)에 요청, 결과로 돌아온 **key**를  
HTTP Request의 Header `Authorization`에 `Token <key>`값을 넣어 전송
```
Authorization: Token fs8943eu342cf79d8933jkd
``` 
'''
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'HTTP Basic Auth (RFC 7617)',
            'description': BASIC_DESCRIPTION,
        },
        'Token': {
            'type': 'DRF AuthToken',
            'description': TOKEN_DESCRIPTION,
        }
    }
}

ROOT_URLCONF = 'config.urls'
LOGIN_REDIRECT_URL = '/accounts/list'
LOGOUT_REDIRECT_URL = '/accounts/list'

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
            ],
        },
    },
]

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = SECRETS['DATABASES']

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
