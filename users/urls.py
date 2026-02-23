from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users import views
from users.apps import UsersConfig
from users.views import UserRegisterView, confirm_email

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path(
        "logout/",
        LogoutView.as_view(template_name="users/logged_out.html"),
        name="logout",
    ),
    path("register/", UserRegisterView.as_view(), name="user_form"),
    path("confirm-email/<str:token>/", confirm_email, name="confirm-email"),
    path("reset-password/", views.reset_password, name="reset_password"),
]
