from django.contrib.auth.models import User


def setup_project_user(user: User, sso_data: dict) -> None:
    """
    Personnalise l'utilisateur Django après login via SSOwat.
    - Récupère les données du header SSO
    - Assigne au groupe par défaut
    - Active l'accès à l’admin Django
    """
    if sso_data:
        user.email = sso_data.get("email", "") or user.email
        user.first_name = sso_data.get("first_name", "") or user.first_name
        user.last_name = sso_data.get("last_name", "") or user.last_name

    # Permet l'accès à l'admin Django
    user.is_staff = True
    user.save()
