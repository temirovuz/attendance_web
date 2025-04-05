from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.validators import validate_international_phonenumber


class UserRegistrationForm(forms.Form):
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "+998947999898"}),
        validators=[validate_international_phonenumber],
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"})
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Parollar mos kelmadi.")

        return cleaned_data


class PhoneLoginForm(forms.Form):
    phone_number = PhoneNumberField(
        widget=forms.TextInput(attrs={"placeholder": "+998947999898 "})
    )
    password = forms.CharField(widget=forms.PasswordInput())
