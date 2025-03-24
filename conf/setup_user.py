from django.contrib.auth.models import User


def setup_project_user(user, sso_data=None):
    """
    Configure les utilisateurs SSO :
    - Si dans le groupe YunoHost 'admins' → superuser + staff
    - Sinon → utilisateur normal
    """
    if sso_data:
        user.email = sso_data.get("email", "") or user.email
        user.first_name = sso_data.get("first_name", "") or user.first_name
        user.last_name = sso_data.get("last_name", "") or user.last_name

        groups = sso_data.get("groups", [])  # ← récupère les groupes YunoHost
        if isinstance(groups, str):  # au cas où c’est une string CSV
            groups = [g.strip() for g in groups.split(",")]

        if "admins" in groups:
            user.is_superuser = True
            user.is_staff = True
        else:
            user.is_superuser = False
            user.is_staff = False

    user.is_active = True
    user.save()
    return user
