from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from account.forms import UserRegistrationForm, PhoneLoginForm
from account.models import CustomUser
from employee.permissions import IsAdminUserAndAuthenticated
from django.contrib.auth import logout


class RegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, "register.html", {"form": form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        
        if not form.is_valid():
            print(form.errors)  # Xatolarni tekshirish uchun
            return render(request, "register.html", {"form": form})
        
        phone_number = form.cleaned_data["phone_number"]
        password = form.cleaned_data["password1"]

        # Agar user allaqachon mavjud bo‘lsa, yaratmaslik
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            print("Bu telefon raqam allaqachon ro‘yxatdan o‘tgan.")
            form.add_error("phone_number", "Bu telefon raqam allaqachon ro‘yxatdan o‘tgan.")
            return render(request, "register.html", {"form": form})

        user = CustomUser(phone_number=phone_number)
        user.set_password(password)
        user.save()

        return redirect("account:login")


class LoginView(View):
    def get(self, request):
        form = PhoneLoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = PhoneLoginForm(request.POST)
        print(form.data)
        print(form.is_valid())
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            password = form.cleaned_data["password"]
            user = authenticate(request, phone_number=phone_number, password=password)

            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                form.add_error(None, "Invalid phone number or password")

        return render(request, "login.html", {"form": form})


class HomeView(IsAdminUserAndAuthenticated,View):
    def get(self, request):
        return render(request, "home.html")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("account:login")