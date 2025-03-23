import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

# ─────────────────────────────
# UTILITIES
# ─────────────────────────────

def get_env(var_name, default=None, required=False):
    value = os.environ.get(var_name, default)
    if required and value is None:
        raise ImproperlyConfigured(f"Missing required environment variable: {var_name}")
    return value

# ─────────────────────────────
# BASE DIR
# ─────────────────────────────

BASE_DIR = Path(__file__).resolve().parent.parent

# ─────────────────────────────
# SECURITY
# ─────────────────────────────

SECRET_KEY = get_env("DJANGO_SECRET_KEY", required=True)
DEBUG = get_env("DJANGO_DEBUG", "False").lower() in ("true", "1", "yes")
ALLOWED_HOSTS = get_env("DJANGO_ALLOWED_HOSTS", "*").split(",")

# ─────────────────────────────
# APPS & MIDDLEWARE
# ─────────────────────────────

INSTALLED_APPS = [
    'bom.apps.BomConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'materializecssform',
    'social_django',
    'djmoney',
    'djmoney.contrib.exchange',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'bom.urls'
WSGI_APPLICATION = 'bom.wsgi.application'

# ─────────────────────────────
# TEMPLATES
# ─────────────────────────────

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'bom/templates/bom'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'bom.context_processors.bom_config',
            ],
        },
    },
]

# ─────────────────────────────
# DATABASE
# ─────────────────────────────

DATABASES = {
    'default': {
        'ENGINE': get_env("DJANGO_DB_ENGINE", "django.db.backends.sqlite3"),
        'NAME': get_env("DJANGO_DB_NAME", BASE_DIR / 'db.sqlite3'),
        'USER': get_env("DJANGO_DB_USER", ""),
        'PASSWORD': get_env("DJANGO_DB_PASSWORD", ""),
        'HOST': get_env("DJANGO_DB_HOST", ""),
        'PORT': get_env("DJANGO_DB_PORT", ""),
    }
}

# ─────────────────────────────
# AUTH
# ─────────────────────────────

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.google.GoogleOAuth',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# ─────────────────────────────
# I18N
# ─────────────────────────────

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ─────────────────────────────
# STATIC & MEDIA
# ─────────────────────────────

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'

# ─────────────────────────────
# LOGIN / REDIRECTS
# ─────────────────────────────

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# ─────────────────────────────
# SOCIAL AUTH
# ─────────────────────────────

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/settings?tab_anchor=file'
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/settings?tab_anchor=file'
SOCIAL_AUTH_LOGIN_ERROR_URL = '/'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = get_env("GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = get_env("GOOGLE_OAUTH2_SECRET")

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'email', 'profile',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/plus.login'
]
SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {
    'access_type': 'offline',
    'approval_prompt': 'force'
}

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'bom.third_party_apis.google_drive.initialize_parent',
)

SOCIAL_AUTH_DISCONNECT_PIPELINE = (
    'social_core.pipeline.disconnect.allowed_to_disconnect',
    'bom.third_party_apis.google_drive.uninitialize_parent',
    'social_core.pipeline.disconnect.get_entries',
    'social_core.pipeline.disconnect.revoke_tokens',
    'social_core.pipeline.disconnect.disconnect',
)

# ─────────────────────────────
# EMAIL
# ─────────────────────────────

EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
SENDGRID_API_KEY = get_env("SENDGRID_API_KEY", required=True)

# ─────────────────────────────
# DJANGO-MONEY
# ─────────────────────────────

CURRENCY_DECIMAL_PLACES = 4
EXCHANGE_BACKEND = 'djmoney.contrib.exchange.backends.FixerBackend'
FIXER_ACCESS_KEY = get_env("FIXER_ACCESS_KEY", required=True)

# ─────────────────────────────
# LOGGING
# ─────────────────────────────

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'logfile': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(os.environ.get("DJANGO_LOGFILE_DIR", BASE_DIR), 'django.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['logfile'],
            'level': get_env("DJANGO_LOG_LEVEL", "INFO"),
            'propagate': False,
        },
        'bom': {
            'handlers': ['logfile'],
            'level': get_env("DJANGO_LOG_LEVEL", "INFO"),
            'propagate': False,
        },
    },
}

# ─────────────────────────────
# BOM CONFIG
# ─────────────────────────────

BOM_CONFIG = {
    'base_template': 'base.html',
    'mouser_api_key': get_env("MOUSER_API_KEY", None),
    'admin_dashboard': {
        'enable_autocomplete': get_env("BOM_AUTOCOMPLETE", "true").lower() in ("true", "1", "yes"),
        'page_size': int(get_env("BOM_PAGE_SIZE", 50)),
    }
}

BOM_LOGIN_URL = None
