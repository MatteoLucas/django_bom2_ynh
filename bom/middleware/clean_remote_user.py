class clean_remote_user:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        remote_user = request.META.get('HTTP_REMOTE_USER', '')
        if ',' in remote_user:
            request.META['HTTP_REMOTE_USER'] = remote_user.split(',')[0]
        return self.get_response(request)
