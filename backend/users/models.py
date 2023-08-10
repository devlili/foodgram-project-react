from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Кастомная модель пользователя на основе AbstractUser.

    Поля:
    - username (str): Имя пользователя (уникальное поле).
    - password (str): Пароль пользователя.
    - email (str): Email пользователя (уникальное поле).
    - first_name (str): Имя пользователя.
    - last_name (str): Фамилия пользователя.

    """

    email = models.EmailField("Почта", unique=True, max_length=254)
    first_name = models.CharField("Имя", max_length=150)
    last_name = models.CharField("Фамилия", max_length=150)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username
