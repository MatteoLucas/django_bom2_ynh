import os

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Secret key (injectée automatiquement pendant l'installation par YunoHost)
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "changeme")

# Mode debug (False en prod !)
DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() in ("true", "1")

# Autorise tous les hôtes — à restreindre si besoin
ALLOWED_HOSTS = ['*']

# Configuration spécifique à django-bom
BOM_CONFIG = {
    'mouser_api_key': os.environ.get("MOUSER_API_KEY", "changeme"),
    'admin_dashboard': {
        'enable_autocomplete': False,
        'page_size': 50,
    }
}

# Google OAuth
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get("GOOGLE_OAUTH2_KEY", "changeme")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get("GOOGLE_OAUTH2_SECRET", "changeme")

# Base de données SQLite par défaut (à adapter en prod)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# SendGrid email backend
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "changeme")

# Clé pour fixer.io (conversions de devises)
FIXER_ACCESS_KEY = os.environ.get("FIXER_ACCESS_KEY", "changeme")
