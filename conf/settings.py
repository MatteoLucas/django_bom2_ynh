import os
from django.core.exceptions import ImproperlyConfigured
import dj_database_url
from django_yunohost_integration.base_settings import *  # noqa
from django_yunohost_integration.secret_key import get_or_create_secret
from pathlib import Path

YNH_SETUP_USER = 'setup_user.setup_project_user'


# SSO-ready secret key file
DATA_DIR_PATH = Path('/home/yunohost.app/django-bom')  # ou injecté par templating
SECRET_KEY = get_or_create_secret(DATA_DIR_PATH / 'secret.txt')

# ... variables env, BASE_DIR, DEBUG etc ...

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
    'django_yunohost_integration',  # ✅ Ajout
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_yunohost_integration.sso_auth.auth_middleware.SSOwatRemoteUserMiddleware',  # ✅ Ajout
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'django_yunohost_integration.sso_auth.auth_backend.SSOwatUserBackend',  # ✅ Ajout SSO en premier
    'django.contrib.auth.backends.ModelBackend',
)

# ✅ Redirection vers SSO
LOGIN_URL = '/yunohost/sso/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/yunohost/sso/'

# Social Auth Google
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = get_env("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY", "")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = get_env("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET", "")
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'email', 'profile',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/plus.login',
]
SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {
    'access_type': 'offline',
    'approval_prompt': 'force',
}

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/settings?tab_anchor=file'
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/settings?tab_anchor=file'
SOCIAL_AUTH_LOGIN_ERROR_URL = '/'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'django.contrib.auth.backends.ModelBackend',
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

# django-money
CURRENCY_DECIMAL_PLACES = 4
EXCHANGE_BACKEND = 'djmoney.contrib.exchange.backends.FixerBackend'
FIXER_ACCESS_KEY = get_env("FIXER_ACCESS_KEY", required=True)

# SendGrid email
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
SENDGRID_API_KEY = get_env("SENDGRID_API_KEY", required=True)


DEBUG = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
            'include_html': True,
        },
        'logfile': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(os.environ.get("DJANGO_LOGFILE_DIR", BASE_DIR), 'django.log'),
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['logfile'],
            'level': get_env("LOG_LEVEL", "WARNING"),
            'propagate': False,
        },
        'bom': {
            'handlers': ['logfile'],
            'level': get_env("LOG_LEVEL", "INFO"),
            'propagate': False,
        },
    },
}

# App spécifique
BOM_CONFIG = {
    'mouser_api_key': None,
    'admin_dashboard': {
        'enable_autocomplete': True,
        'page_size': 50,
    }
}

BOM_LOGIN_URL = None
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
