from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
)

from users.models import User


class StyledFormMixin:
    """Добавляет Bootstrap-стили полям формы."""

    def add_styles(self) -> None:
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class UserRegisterForm(StyledFormMixin, UserCreationForm):
    """Форма регистрации пользователя."""

    class Meta:
        model = User
        fields = (
            "email",
            "phone",
            "country",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_styles()


class UserLoginForm(StyledFormMixin, AuthenticationForm):
    """Форма входа по электронной почте."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].label = "Электронная почта"
        self.fields["username"].widget = forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "example@mail.ru",
                "autocomplete": "email",
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Пароль",
            }
        )


class UserProfileForm(StyledFormMixin, forms.ModelForm):
    """Форма редактирования профиля."""

    class Meta:
        model = User
        fields = (
            "email",
            "avatar",
            "phone",
            "country",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_styles()