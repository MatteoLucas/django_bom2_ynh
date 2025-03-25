class CleanRemoteUserMiddleware:
    """
    Nettoie la variable HTTP_REMOTE_USER si elle contient un doublon, ex: 'mlucas,mlucas'.
    À placer avant SSOwatRemoteUserMiddleware.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        remote_user = request.META.get("HTTP_REMOTE_USER")
        if remote_user and "," in remote_user:
            cleaned_user = remote_user.split(",")[0].strip()
            request.META["HTTP_REMOTE_USER"] = cleaned_user
        return self.get_response(request)
