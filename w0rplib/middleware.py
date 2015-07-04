startup_time = None


class StartupTimeMiddleware:
    """
    This middleware sets the startup_time for the app in the request object,
    such that views can all access the startup_time.
    """
    def process_request(self, request):
        request.startup_time = startup_time
