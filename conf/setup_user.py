from django.contrib.auth.models import User
from inventory.permissions import get_or_create_normal_user_group


def setup_project_user(user: User, sso_data: dict) -> None:
    """
    Personnalise l'utilisateur Django après login via SSOwat.
    - Récupère les données du header SSO
    - Assigne au groupe par défaut
    - Active l'accès à l’admin Django
    """
    user.email = sso_data.get("email", "") or user.email
    user.first_name = sso_data.get("first_name", "") or user.first_name
    user.last_name = sso_data.get("last_name", "") or user.last_name

    # Ajoute au groupe "normal user" si nécessaire
    pyinventory_user_group = get_or_create_normal_user_group()[0]
    user.groups.set([pyinventory_user_group])

    user.is_staff = True
    user.save()
