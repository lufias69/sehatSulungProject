"""
Production settings module for sehatSulungProject.
"""

import os
import environ
from pathlib import Path
from datetime import timedelta

# Baca .env.prod
env = environ.Env()
environ.Env.read_env(os.path.join(Path(__file__).resolve().parent.parent, ".env.prod"))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Create log directory if not exists
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", default=True)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")

# SECURITY WARNING: use proper allowed hosts in production
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS", default=[])

# Security middleware
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = "DENY"
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    # Apps
    'admin_app.apps.AdminAppConfig',
    'regional_data_app.apps.RegionalDataAppConfig',
    'health_data_app.apps.HealthDataAppConfig',
    'fitur_app.apps.FiturAppConfig',
    'question_app.apps.QuestionAppConfig',
    'media_center_app.apps.MediaCenterAppConfig',
    'checkup_app.apps.CheckupAppConfig',
    'alamat_app.apps.AlamatAppConfig',
    'session_app.apps.SessionAppConfig',
    'task_app.apps.TaskAppConfig',
    'analisis_ai.apps.AnalisisAiConfig',
    'hash_app.apps.HashAppConfig',

    # Third-party
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'cloudinary_storage',
    'cloudinary',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "sehatSulungProject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "allauth.account.context_processors.account",
                "allauth.socialaccount.context_processors.socialaccount",
            ],
        },
    },
]

WSGI_APPLICATION = "sehatSulungProject.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": env("POSTGRES_PORT", default="5432"),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_ROOT = "/app/staticfiles"
STATIC_URL = "/static/"

# Media files
MEDIA_ROOT = "/app/media"
MEDIA_URL = "/media/"

# Email configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = env.int("EMAIL_PORT", 587)
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", True)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", "")

# REST Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

# Simple JWT Settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

# Allauth Settings
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

SITE_ID = 1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "none"

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env("GOOGLE_CLIENT_ID", "")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env("GOOGLE_CLIENT_SECRET", "")

# Cloudinary Storage
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env("CLOUDINARY_NAME"),
    'API_KEY': env("CLOUDINARY_API_KEY"),
    'API_SECRET': env("CLOUDINARY_API_SECRET"),
}

DEFAULT_FILE_STORAGE = 'cloudinary.storage.MediaCloudinaryStorage'

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_DIR, "django_errors.log"),
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}


# """
# Production settings module for sehatSulungProject.
# """
#
# import os
# from datetime import timedelta
# from pathlib import Path
# from dotenv import load_dotenv
# import environ
# BASE_DIR = Path(__file__).resolve().parent.parent
# env = environ.Env()
# environ.Env.read_env(os.path.join(BASE_DIR, '.env.prod'))
# # load_dotenv()
#
# # Build paths inside the project like this: BASE_DIR / 'subdir'.
#
#
# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'
#
# # SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', "django-insecure-v-_b*)$++itqwkcdj@3@eae4)^g(v@+mmjh_mp41@k0+o_-z37")
#
# # SECURITY WARNING: use proper allowed hosts in production
# ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
#
# # Production-specific CORS and CSRF settings (optional but recommended)
# CSRF_TRUSTED_ORIGINS = os.getenv('DJANGO_CSRF_TRUSTED_ORIGINS', 'https://*.yourdomain.com').split(',')
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
#
# # Application definition
# INSTALLED_APPS = [
#     "django.contrib.admin",
#     "django.contrib.auth",
#     "django.contrib.contenttypes",
#     "django.contrib.sessions",
#     "django.contrib.messages",
#     "django.contrib.staticfiles",
#     "django.contrib.sites",
#
#     # Apps
#     'admin_app.apps.AdminAppConfig',
#     'regional_data_app.apps.RegionalDataAppConfig',
#     'health_data_app.apps.HealthDataAppConfig',
#     'fitur_app.apps.FiturAppConfig',
#     'question_app.apps.QuestionAppConfig',
#     'media_center_app.apps.MediaCenterAppConfig',
#     'checkup_app.apps.CheckupAppConfig',
#     'alamat_app.apps.AlamatAppConfig',
#     'session_app.apps.SessionAppConfig',
#     'task_app.apps.TaskAppConfig',
#     'analisis_ai.apps.AnalisisAiConfig',
#     'hash_app.apps.HashAppConfig',
#
#     # Third-party
#     'rest_framework',
#     'rest_framework.authtoken',
#     'rest_framework_simplejwt',
#     'rest_framework_simplejwt.token_blacklist',
#     'allauth',
#     'allauth.account',
#     'allauth.socialaccount',
#     'allauth.socialaccount.providers.google',
# ]
#
# MIDDLEWARE = [
#     "django.middleware.security.SecurityMiddleware",
#     "django.contrib.sessions.middleware.SessionMiddleware",
#     "django.middleware.common.CommonMiddleware",
#     "django.middleware.csrf.CsrfViewMiddleware",
#     "django.contrib.auth.middleware.AuthenticationMiddleware",
#     "django.contrib.messages.middleware.MessageMiddleware",
#     "django.middleware.clickjacking.XFrameOptionsMiddleware",
#     "allauth.account.middleware.AccountMiddleware",
# ]
#
# ROOT_URLCONF = "sehatSulungProject.urls"
#
# TEMPLATES = [
#     {
#         "BACKEND": "django.template.backends.django.DjangoTemplates",
#         "DIRS": [BASE_DIR / 'templates'],
#         "APP_DIRS": True,
#         "OPTIONS": {
#             "context_processors": [
#                 "django.template.context_processors.debug",
#                 "django.template.context_processors.request",
#                 "django.contrib.auth.context_processors.auth",
#                 "django.contrib.messages.context_processors.messages",
#                 "allauth.account.context_processors.account",
#                 "allauth.socialaccount.context_processors.socialaccount",
#             ],
#         },
#     },
# ]
#
# WSGI_APPLICATION = "sehatSulungProject.wsgi.application"
#
# # Database
# # https://docs.djangoproject.com/en/5.2/ref/settings/#databases
#
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": os.getenv("POSTGRES_DB", "mydb"),
#         "USER": os.getenv("POSTGRES_USER", "myuser"),
#         "PASSWORD": os.getenv("POSTGRES_PASSWORD", "mypassword"),
#         "HOST": os.getenv("POSTGRES_HOST", "db"),
#         "PORT": os.getenv("POSTGRES_PORT", "5432"),
#     }
# }
#
# # Password validation
# #  https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators
#
# AUTH_PASSWORD_VALIDATORS = [
#     {
#         "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
#     },
#     {
#         "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
#     },
#     {
#         "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
#     },
#     {
#         "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
#     },
# ]
#
# # Internationalization
# LANGUAGE_CODE = "en-us"
# TIME_ZONE = "UTC"
# USE_I18N = True
# USE_TZ = True
#
# # Static files (CSS, JavaScript, Images)
# STATIC_ROOT = "/app/staticfiles"#os.path.join(BASE_DIR, "staticfiles")
# STATIC_URL = "/static/"
#
# # Media files
# MEDIA_ROOT = "/app/media"
# MEDIA_URL = "/media/"#"/media/"
#
# # Email configuration (example using SMTP)
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
# EMAIL_PORT = os.getenv("EMAIL_PORT", 587)
# EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
# EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
#
# # Django REST Framework
# REST_FRAMEWORK = {
#     "DEFAULT_AUTHENTICATION_CLASSES": (
#         "rest_framework.authentication.TokenAuthentication",
#         "rest_framework.authentication.SessionAuthentication",
#     ),
#     "DEFAULT_PERMISSION_CLASSES": [
#         "rest_framework.permissions.IsAuthenticated",
#     ],
# }
#
# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=365*100),
#     "UPDATE_LAST_LOGIN": True,
#     "ALGORITHM": "HS256",
#     "SIGNING_KEY": SECRET_KEY,
#     "VERIFYING_KEY": None,
#     "AUDIENCE": None,
#     "ISSUER": None,
#     "JWK_URL": None,
#     "LEEWAY": 0,
#     "AUTH_HEADER_TYPES": ("Bearer",),
#     "ROTATE_REFRESH_TOKENS": True,
#     "BLACKLIST_AFTER_ROTATION": True,
# }
#
# # Allauth configuration
# AUTHENTICATION_BACKENDS = (
#     "django.contrib.auth.backends.ModelBackend",
#     "allauth.account.auth_backends.AuthenticationBackend",
# )
#
# SITE_ID = 1
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_USERNAME_REQUIRED = False
# ACCOUNT_SESSION_REMEMBER = True
# ACCOUNT_AUTHENTICATION_METHOD = "email"
# ACCOUNT_EMAIL_VERIFICATION = "none"
#
# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv("GOOGLE_CLIENT_ID")
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
#
# # Security settings
# SECURE_SSL_REDIRECT = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# X_FRAME_OPTIONS = "DENY"
# SECURE_HSTS_SECONDS = 31536000  # 1 year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_BROWSER_XSS_FILTER = True
#
# # Logging (optional, recommended for production)
# # Di prod.py, setelah BASE_DIR
# LOG_DIR = os.path.join(BASE_DIR, "logs")
# os.makedirs(LOG_DIR, exist_ok=True)
#
# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "handlers": {
#         "file": {
#             "level": "ERROR",
#             "class": "logging.FileHandler",
#             "filename": os.path.join(BASE_DIR, "logs", "django_errors.log"),
#         },
#     },
#     "loggers": {
#         "django": {
#             "handlers": ["file"],
#             "level": "ERROR",
#             "propagate": True,
#         },
#     },
# }
#
#
# CLOUDINARY_STORAGE = {
#     'CLOUD_NAME': os.getenv('CLOUDINARY_NAME'),
#     'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
#     'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
# }
#
# DEFAULT_FILE_STORAGE = 'cloudinary.storage.MediaCloudinaryStorage'
