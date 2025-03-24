def setup_project_user(user, sso_data):
    """
    Initialiser les nouveaux utilisateurs créés via SSOwat.
    """
    user.email = sso_data.get("email", "") or user.email
    user.first_name = sso_data.get("first_name", "") or user.first_name
    user.last_name = sso_data.get("last_name", "") or user.last_name

    if user.username == "mlucas":
        user.is_superuser = True
        user.is_staff = True
    else:
        user.is_superuser = False
        user.is_staff = False

    user.save()
    return user
