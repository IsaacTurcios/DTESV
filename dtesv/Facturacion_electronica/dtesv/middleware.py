from django.contrib.auth import logout

class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Verificar si la cookie de sesión está presente
        if not request.COOKIES.get('sessionid') and request.user.is_authenticated:
            logout(request)

        return response