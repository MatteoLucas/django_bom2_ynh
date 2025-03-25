class CleanRemoteUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.META.get("REMOTE_USER"):
            request.META["REMOTE_USER"] = request.META["REMOTE_USER"].split(",")[0]
        return self.get_response(request)