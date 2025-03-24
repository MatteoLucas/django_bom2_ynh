from django.contrib.auth.models import User


def setup_project_user(user, sso_data: dict):
    user.email = sso_data.get("email", "") or user.email
    user.first_name = sso_data.get("first_name", "") or user.first_name
    user.last_name = sso_data.get("last_name", "") or user.last_name

    # Seul l'utilisateur admin défini à l'installation est superuser
    from django.conf import settings
    admin_username = settings.get_env("ADMIN_USERNAME", None)
    if user.username == admin_username:
        user.is_superuser = True
        user.is_staff = True
    else:
        user.is_superuser = False
        user.is_staff = False

    user.save()
    return user