import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import (
    UserLoginForm,
    UserProfileForm,
    UserRegisterForm,
)
from users.models import User


logger = logging.getLogger(__name__)


class UserRegisterView(CreateView):
    """Регистрирует нового пользователя."""

    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        response = super().form_valid(form)

        try:
            send_mail(
                subject="Добро пожаловать в SkyStore!",
                message=(
                    "Регистрация успешно завершена. "
                    "Теперь вы можете войти в SkyStore."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.object.email],
                fail_silently=False,
            )

            messages.success(
                self.request,
                "Регистрация завершена. "
                "Приветственное письмо отправлено.",
            )

        except Exception:
            logger.exception(
                "Не удалось отправить приветственное письмо."
            )

            messages.warning(
                self.request,
                "Аккаунт создан, но письмо отправить не удалось.",
            )

        return response


class UserLoginView(LoginView):
    """Авторизует пользователя по email и паролю."""

    template_name = "users/login.html"
    authentication_form = UserLoginForm
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    """Завершает сеанс пользователя."""

    next_page = reverse_lazy("home")


class UserProfileUpdateView(
    LoginRequiredMixin,
    UpdateView,
):
    """Редактирует профиль текущего пользователя."""

    model = User
    form_class = UserProfileForm
    template_name = "users/profile_form.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(
            self.request,
            "Профиль успешно обновлён.",
        )

        return super().form_valid(form)