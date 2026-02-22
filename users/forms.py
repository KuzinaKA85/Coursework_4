from django.contrib.auth.forms import UserCreationForm

from newsletter.mixins import AllFormMixin
from users.models import User


class UserRegisterForm(AllFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "password1", "password2"]
