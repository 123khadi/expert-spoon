
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

import os

CONFIG_PATH = BASE_DIR / 'whatsapp_config.txt'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@)--j7i64w)ihq2%=y#_mcvc-dkl#e$tj$i8o*52z(zou+0ymf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'incidents',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
]
SITE_ID = 1

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'APP': {
            'client_id': '1623481185881775',
            'secret': 'KHANstar@2026',
        },
        'METHOD': 'oauth2',
        'SCOPE': ['khadijayaq779@outlook.com', 'public_profile'],
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'rapidsop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'incidents' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rapidsop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.1/howto/static-files/

STATIC_URL = 'static/'


# Email
# https://docs.djangoproject.com/en/6.1/topics/email/#topic-email-configuration

MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}
LOGIN_REDIRECT_URL = '/dashboard/'
ACCOUNT_LOGOUT_ON_GET = True
SOCIALACCOUNT_ADAPTER = 'incidents.adapter.CustomSocialAccountAdapter'
STATIC_ROOT = BASE_DIR / 'staticfiles'
#whatsApp API Configuration RapidSOP Mardan
WHATSAPP_API_URL = "https://graph.facebook.com/v19.0/1365976849934714/messages"
WHATSAPP_PHONE_NUMBER = "1365976849934714"
WHATSAPP_BUSINESS_ID = "1859457492075624"
WHATSAPP_TOKEN = "EAAaD9pkdAm4BSs7oNmZCu025tG90WQGDLwxCr2gpS9bzNQXP0q5wvfiNC7XxjOz55qGX4VBK4jrP2jJy1ZB4CFAfrCguXJj7iPsiZAVv74JNlQCH2pj5NGwD2r8EZBlk0PckZBbpnR92B0jwqPTrdvf17poOZAL94cLI6khOTvdIEA5VIF9znsImPLodlebfiZAuH8rNOlrL2jXLDISSnBEvUZBC0Hvi0cE530Cfv6gsUW5i7gAKqmRJE4CjXi1BHw4Uyukg8wiZBlrnzCz94OnpX"
if CONFIG_PATH.exists():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        WHATSAPP_TOKEN = f.read().strip()
CSRF_TRUSTED_ORIGINS = ['https://erratic-plywood-unthawed.ngrok-free.dev', 'https://*.ngrok-free.dev']
