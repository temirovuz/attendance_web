from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

class LogoutRedirectMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print('kirdi')
        allowed_paths = ['/account/login/', '/admin/login/', '/static/', 'account/register/']
        if request.path == '/account/register/':
            return redirect('/account/register/')
        if not request.user.is_authenticated and request.path not in allowed_paths:
            return redirect('/account/login/')
