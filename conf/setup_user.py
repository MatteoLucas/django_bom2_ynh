from inventory.permissions import get_or_create_normal_user_group


def setup_project_user(user):
    """
    Configure les utilisateurs pour django-bom.
    Fonction appelée par django_yunohost_integration.sso_auth
    """
    # Tous les utilisateurs auront accès à l'interface d'administration
    user.is_staff = True
    user.save()
    return user
