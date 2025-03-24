from django.contrib.auth.models import User


def setup_project_user(user, sso_data: dict = None):
    """
    Setup basic user profile from SSO data.
    """
    if sso_data:
        user.email = sso_data.get("email", "") or user.email
        user.first_name = sso_data.get("first_name", "") or user.first_name
        user.last_name = sso_data.get("last_name", "") or user.last_name

    # Permet l'accès à l'admin Django
    user.is_staff = True
    user.save()
    return user