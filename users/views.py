import secrets

from django.contrib import messages

from django.core.mail import send_mail
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse

from django.views.generic import CreateView

from config import settings

from users.forms import UserRegisterForm, PasswordResetForm
from users.models import User


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()

        host = self.request.get_host()
        url = f"https://{host}/users/confirm-email/{token}/"

        send_mail(
            subject="Подтверждение регистрации",
            message=f"Для подтверждения перейдите по ссылке: {url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        return super().form_valid(form)


def confirm_email(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


def reset_password(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.filter(email=email).first()

            if user:
                new_password = secrets.token_hex(8)
                user.set_password(new_password)
                user.save()

                send_mail(
                    subject="Восстановление пароля",
                    message=f"Ваш новый пароль: {new_password}",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                )
                messages.success(request, "Новый пароль отправлен на вашу почту.")
                return redirect(reverse("users:login"))
            else:
                messages.error(request, "Пользователь с таким email не найден.")
    else:
        form = PasswordResetForm()

    return render(request, "users/reset_password.html", {"form": form})


# class UserLoginView(LoginView):
#     template_name = 'users/login.html'
#     form_class = StyledLoginForm
#
#     def get_success_url(self):
#         return reverse_lazy('web_app:main')
#
#
# class UserLogoutView(LogoutView):
#     def get(self, request, *args, **kwargs):
#         return self.post(request, *args, **kwargs)
