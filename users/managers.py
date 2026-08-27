from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """Создаёт обычных пользователей и суперпользователей."""

    use_in_migrations = True

    def create_user(
        self,
        email: str,
        password: str | None = None,
        **extra_fields,
    ):
        if not email:
            raise ValueError(
                "Пользователь должен указать электронную почту."
            )

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(
        self,
        email: str,
        password: str | None = None,
        **extra_fields,
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields["is_staff"] is not True:
            raise ValueError(
                "Суперпользователь должен иметь is_staff=True."
            )

        if extra_fields["is_superuser"] is not True:
            raise ValueError(
                "Суперпользователь должен иметь is_superuser=True."
            )

        return self.create_user(
            email,
            password,
            **extra_fields,
        )