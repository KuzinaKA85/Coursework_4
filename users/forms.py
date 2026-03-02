from django.contrib.auth.forms import UserCreationForm
from django import forms

from newsletter.mixins import AllFormMixin
from users.models import User


class UserRegisterForm(AllFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "password1", "password2"]


class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Введите ваш email"}
        ),
    )
