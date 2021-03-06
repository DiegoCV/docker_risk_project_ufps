"""
Django settings for Risk_project project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nk8@)vil_l(_guo+$=!=*@59zl5$=h7w6z^hvdc03j&v@rgdzp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Risk_project_ufps',
    #'django_extensions',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Risk_project.urls'

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

WSGI_APPLICATION = 'Risk_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
'default': {
          'ENGINE':'django.db.backends.mysql',
           'OPTIONS':{
            'sql_mode':'STRICT_TRANS_TABLES',
            },
           'NAME':os.environ['DEFAULT_NAME'],
           'USER':os.environ['DEFAULT_USER'],
           'PASSWORD':os.environ['DEFAULT_PASSWORD'],
           'HOST':os.environ['DEFAULT_HOST'],
           'PORT':os.environ['DEFAULT_PORT'],
    },
    'riesgos': {
            'ENGINE':'django.db.backends.mysql',
            'OPTIONS':{
            'sql_mode':'STRICT_ALL_TABLES',
            },
            'NAME':os.environ['RIESGOS_NAME'],
            'USER':os.environ['RIESGOS_USER'],
            'PASSWORD':os.environ['RIESGOS_PASSWORD'],
            'HOST':os.environ['RIESGOS_HOST'],
            'PORT':os.environ['RIESGOS_PORT'],
    },
    'base': {
            'ENGINE':'django.db.backends.mysql',
            'OPTIONS':{
            'sql_mode':'STRICT_ALL_TABLES',
            },
            'NAME':os.environ['BASE_NAME'],
            'USER':os.environ['BASE_USER'],
            'PASSWORD':os.environ['BASE_PASSWORD'],
            'HOST':os.environ['BASE_HOST'],
            'PORT':os.environ['BASE_PORT'],
    },
}

DATABASE_ROUTERS = ['Risk_project.AuthRouter.AuthRouter']

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

#LANGUAGE_CODE = 'en-us'

LANGUAGE_CODE = 'es-eu'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-file
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    # '/static'
]

STATIC_ROOT = '/static' #os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

"""STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
    BASE_DIR + "static",
    'Risk_project_ufps/static/',
]"""

# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = '/inicio/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

EMAIL_USE_TLS=True
EMAIL_HOST=os.environ['EMAIL_HOST'] 
EMAIL_PORT=os.environ['EMAIL_PORT']
EMAIL_HOST_USER=os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD =os.environ['EMAIL_HOST_PASSWORD']
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
