# core/middleware.py
from django.contrib import messages
from django.shortcuts import redirect
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class LoginRequiredMiddleware:
    """
    Middleware, который заставляет пользователей авторизоваться
    перед доступом к любым защищённым маршрутам.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [
            '/',
            '/login/',
            '/users/',
            '/users/create/',
            '/admin/',
            '/admin/login/'
            '/favicon.ico'
        ]

    def __call__(self, request):
        if not request.user.is_authenticated:
            path = request.path_info
            if not any(path == url for url in self.exempt_urls) and not path.startswith('/static/'):
                messages.error(request, _("You are not logged in! Please log in."))
                return redirect(settings.LOGIN_URL)
        return self.get_response(request)