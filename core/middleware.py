from django.shortcuts import redirect
from django.conf import settings
from django.urls import resolve

EXEMPT_URLS = [
    'account:login',  # login sahifa
    'account:logout',  # logout sahifa
    'admin:login',
    'admin:index',
]

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_url = resolve(request.path_info).view_name

        if not request.user.is_authenticated and current_url not in EXEMPT_URLS:
            return redirect(settings.LOGIN_URL)
        
        return self.get_response(request)





class NoCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
