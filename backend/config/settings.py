"""
Django settings for config project.
"""

from decouple import config
from pathlib import Path
import os
import dj_database_url


# ==================================================
# BASE DIRECTORY
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==================================================
# SECURITY
# ==================================================

SECRET_KEY = config(
    'SECRET_KEY',
    default='django-insecure-local-dev-key-change-this'
)

DEBUG = config(
    'DEBUG',
    default=False,
    cast=bool
)

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='*'
).split(',')


# ==================================================
# APPLICATIONS
# ==================================================

INSTALLED_APPS = [

    # DJANGO
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # THIRD PARTY
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',

    # LOCAL APPS
    'movies',
    'accounts',

]


# ==================================================
# MIDDLEWARE
# ==================================================

MIDDLEWARE = [

    # CORS
    'corsheaders.middleware.CorsMiddleware',

    # SECURITY
    'django.middleware.security.SecurityMiddleware',

    # STATIC FILES
    'whitenoise.middleware.WhiteNoiseMiddleware',

    # DJANGO
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]


# ==================================================
# URLS
# ==================================================

ROOT_URLCONF = 'config.urls'


# ==================================================
# TEMPLATES
# ==================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [],

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


# ==================================================
# WSGI
# ==================================================

WSGI_APPLICATION = 'config.wsgi.application'


# ==================================================
# DATABASE
# ==================================================

DATABASES = {

    'default': dj_database_url.config(

        default=config(
            'DATABASE_URL',
            default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
        )

    )

}


# ==================================================
# PASSWORD VALIDATION
# ==================================================

AUTH_PASSWORD_VALIDATORS = [

    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },

    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },

    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },

    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },

]


# ==================================================
# INTERNATIONALIZATION
# ==================================================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# ==================================================
# STATIC FILES
# ==================================================

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(
    BASE_DIR,
    'staticfiles'
)

STATICFILES_STORAGE = (
    'whitenoise.storage.CompressedManifestStaticFilesStorage'
)


# ==================================================
# DEFAULT PRIMARY KEY
# ==================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==================================================
# CORS SETTINGS
# ==================================================

CORS_ALLOWED_ORIGINS = [

    # LOCAL FRONTEND
    "http://localhost:5173",

    "http://127.0.0.1:5173",

]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_ALL_ORIGINS = DEBUG


# ==================================================
# CSRF SETTINGS
# ==================================================

CSRF_TRUSTED_ORIGINS = [

    "https://*.onrender.com",

]


# ==================================================
# DJANGO REST FRAMEWORK
# ==================================================

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (

        'rest_framework_simplejwt.authentication.JWTAuthentication',

    ),

}


# ==================================================
# SECURITY SETTINGS FOR RENDER
# ==================================================

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_COOKIE_SECURE = not DEBUG

CSRF_COOKIE_SECURE = not DEBUG


# ==================================================
# OPTIONAL LOGGING
# ==================================================

LOGGING = {

    'version': 1,

    'disable_existing_loggers': False,

}