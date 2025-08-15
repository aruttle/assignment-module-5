# config/settings.py
import os
from pathlib import Path
from decouple import config
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Secrets & Debug ---
SECRET_KEY = config('SECRET_KEY', default='insecure-secret-key-for-dev')
DEBUG = config('DEBUG', default=True, cast=bool)

# --- Hosts ---
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='assignment-module-5.onrender.com,127.0.0.1,localhost'
).split(',')

# --- Installed Apps ---
INSTALLED_APPS = [
    # Django core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',

    # Cloudinary (order matters: storage before staticfiles)
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',

    # Project apps
    'core',
    'users',
    'bookings',
    # 'projects',  # removed (no module on Render)
    'glamp_projects',
    'glamp_messaging',

    # API
    'rest_framework',
]

# --- DRF ---
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# --- Middleware ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # serve static on Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --- URLs / WSGI / ASGI ---
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# --- Templates ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# --- Database ---
DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'))
}

# --- Auth ---
AUTH_USER_MODEL = 'users.CustomUser'
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- I18N ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Dublin'
USE_I18N = True
USE_TZ = True

# --- Static & Media ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise: simpler non-manifest storage avoids racey 404s
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
WHITENOISE_USE_FINDERS = True

if DEBUG:
    # Local media storage
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'
    STORAGES = {
        'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
        'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
    }
else:
    # Production: Cloudinary for uploaded media
    CLOUDINARY_URL = config('CLOUDINARY_URL')  # set in Render env
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    STORAGES = {
        'default': {'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage'},
        'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
    }

# --- Defaults ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Auth redirects ---
LOGIN_REDIRECT_URL = 'users:profile'
LOGOUT_REDIRECT_URL = 'core:home'
LOGIN_URL = 'users:login'

# --- Security / Proxy ---
CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='https://assignment-module-5.onrender.com,http://localhost:8000,http://127.0.0.1:8000'
).split(',')
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# --- Email (safe defaults for password reset) ---
if DEBUG:
    # Dev: print emails to console so reset links are visible and nothing can fail
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = 'no-reply@example.com'
else:
    # Prod: allow configuring real email via environment variables.
    # If not configured, fall back to console to avoid runtime errors.
    EMAIL_BACKEND = config(
        'EMAIL_BACKEND',
        default='django.core.mail.backends.console.EmailBackend'
    )
    DEFAULT_FROM_EMAIL = config(
        'DEFAULT_FROM_EMAIL',
        default='no-reply@assignment-module-5.onrender.com'
    )
    # Only read SMTP settings if the chosen backend is SMTP
    if EMAIL_BACKEND.endswith('smtp.EmailBackend'):
        EMAIL_HOST = config('EMAIL_HOST', default='')
        EMAIL_PORT = config('EMAIL_PORT', cast=int, default=587)
        EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
        EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
        EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool, default=True)
        EMAIL_USE_SSL = config('EMAIL_USE_SSL', cast=bool, default=False)
