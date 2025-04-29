from pathlib import Path
from os import getenv
from os import path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent



load_env = path.join(BASE_DIR, '.env')
if path.isfile(load_env) :
    load_dotenv(load_env)

print(load_dotenv(load_env))




DJNAGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',]

THIRD_PARTY_APPS =  ['rest_framework', 'corsheaders']

LOCAL_APPS = ['apiapp.apps.ApiappConfig']

INSTALLED_APPS = DJNAGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS








DJANGO_MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',]

LOCAL_MIDDLEWARE =  []

MIDDLEWARE = DJANGO_MIDDLEWARE + LOCAL_MIDDLEWARE


# CORS configuration
# CORS_ALLOWED_ORIGINS = []
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True





#-Rest settings
REST_FRAMEWORK = {}








TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR],
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
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
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









# Django-variables

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

WSGI_APPLICATION = 'main.wsgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

ROOT_URLCONF = 'main.urls'

STATIC_URL = 'static/'

STATIC_DIR = 'static/'

MEDIA_DIR = path.join(BASE_DIR , "media")

MEDIA_URL = '/media/'

MEDIA_ROOT = path.join(BASE_DIR , "media")

ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1']

SECRET_KEY = getenv('SECRET_KEY')

DEBUG = getenv('DEBUG')
