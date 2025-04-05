from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render


class IsAdminUserAndAuthenticated(UserPassesTestMixin):
    """
    Custom permission to allow only authenticated users with user_type 'admin'.
    """

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and getattr(user, "user_type", None) == "admin"

    def handle_no_permission(self):
        """
        Handle the case when the user does not have permission.
        """
        return render(self.request, "errors/not_login.html")