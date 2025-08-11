# config/settings.py
import os
from pathlib import Path
from decouple import config
import dj_database_url

# --- Base Directory ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Secret Key ---
# Pulled from env in both local (.env) and Render
SECRET_KEY = config('SECRET_KEY', default='insecure-secret-key-for-dev')

# --- Debug Mode ---
DEBUG = config('DEBUG', default=True, cast=bool)

# --- Allowed Hosts ---
# Read from env; default includes your Render domain + local hosts
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='assignment-module-5.onrender.com,127.0.0.1,localhost'
).split(',')

# --- Installed Apps ---
INSTALLED_APPS = [
    # Django core apps...
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your apps
    'core',
    'users',
    'bookings',
    'projects',
    'glamp_projects',
    'glamp_messaging',
]

# --- Middleware ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Static files for Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --- Root URL Configuration ---
ROOT_URLCONF = 'config.urls'

# --- Templates ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Global templates folder
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

# --- WSGI / ASGI ---
WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# --- Database ---
DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'))
}

# --- Custom User Model ---
AUTH_USER_MODEL = 'users.CustomUser'

# --- Password Validation ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Language & Timezone ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Dublin'
USE_I18N = True
USE_TZ = True

# --- Static Files ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'  # For Render deployment

# Use Whitenoise's hashed/compressed storage in production
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}

# --- Media Files ---
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# --- Default Primary Key Field ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Login URLs ---
LOGIN_REDIRECT_URL = 'users:profile'
LOGOUT_REDIRECT_URL = 'core:home'
LOGIN_URL = 'users:login'

# --- CSRF Trusted Origins ---
# Read from env; default includes localhost and your Render domain over HTTPS
CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='https://assignment-module-5.onrender.com,http://localhost:8000,http://127.0.0.1:8000'
).split(',')

# (Optional but useful on Render behind proxy/SSL)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
