from django.db import models
from django.contrib.auth import get_user_model
import jwt

from datetime import datetime
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.contrib.auth.models import PermissionsMixin


class User(AbstractBaseUser, PermissionsMixin):
    """
    Определяет наш пользовательский класс User.
    Требуется имя пользователя, адрес электронной почты и пароль.
    """

    username = models.CharField(db_index=True, max_length=255, unique=True)

    email = models.EmailField(
        validators=[validators.validate_email],
        unique=True,
        blank=False
    )

    is_staff = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    # Свойство `USERNAME_FIELD` сообщает нам, какое поле мы будем использовать для входа.
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ('username',)

    # Сообщает Django, что класс UserManager, определенный выше,
    # должен управлять объектами этого типа.
    objects = UserManager()

    def __str__(self):
        """
        Возвращает строковое представление этого `User`.
        Эта строка используется, когда в консоли выводится `User`.
        """
        return self.username

    @property
    def token(self):
        """
        Позволяет нам получить токен пользователя, вызвав `user.token` вместо
        `user.generate_jwt_token().

        Декоратор `@property` выше делает это возможным.
        `token` называется «динамическим свойством ».
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        Этот метод требуется Django для таких вещей,
        как обработка электронной почты.
        Обычно это имя и фамилия пользователя.
        Поскольку мы не храним настоящее имя пользователя,
        мы возвращаем его имя пользователя.
        """
        return self.username

    def get_short_name(self):
        """
        Этот метод требуется Django для таких вещей,
        как обработка электронной почты.
        Как правило, это будет имя пользователя.
        Поскольку мы не храним настоящее имя пользователя,
        мы возвращаем его имя пользователя.
        """
        return self.username

    def _generate_jwt_token(self):
        """
        Создает веб-токен JSON, в котором хранится идентификатор
        этого пользователя и срок его действия
        составляет 60 дней в будущем.
        """
        dt = datetime.now() + timedelta(6000)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


class ApplicationModel(models.Model):
    title = models.CharField(max_length=120, verbose_name="Заголовок")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор заявки", related_name='author')
    text = models.TextField(verbose_name="Содержание")
    date_of_submission = models.DateField(verbose_name="Время отправки", default="2020-10-18")
    priority_types = (
        (1, "Неопределен"),
        (2, "Низкий"),
        (3, "Средний"),
        (4, "Высокий"),
        (5, "Критический"),
    )
    priority = models.IntegerField(choices=priority_types, default=1, verbose_name="Приоритет заявки")
    status_types = (
        (1, "Проверка"),
        (2, "Принята"),
        (3, "В процессе"),
        (4, "Выполнена"),
        (5, "В архиве"),
    )
    status = models.IntegerField(choices=status_types, verbose_name="Статус заявки")

    responsible_staff = models.ForeignKey(User, default=1, on_delete=models.CASCADE, related_name='staff',
                                          verbose_name="Отвественный")

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

#
# class Room(models.Model):
#     """Модель комнаты чата"""
#     # creator = models.ForeignKey(User, verbose_name="Создатель", on_delete=models.CASCADE)
#     # invited = models.ManyToManyField(User, verbose_name="Участники", related_name="invited_user")
#     app = models.ForeignKey(ApplicationModel, verbose_name="Заявка", on_delete=models.CASCADE,)
#     date = models.DateTimeField("Дата создания", auto_now_add=True)
#
#     class Meta:
#         verbose_name = "Комната чата"
#         verbose_name_plural = "Комнаты чатов"


class Chat(models.Model):
    """Модель чата"""
    app = models.ForeignKey(ApplicationModel, verbose_name="Заявка чата", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    text = models.TextField("Сообщение", max_length=500)
    date = models.DateTimeField("Дата отправки", auto_now_add=True)

    class Meta:
        verbose_name = "Сообщение чата"
        verbose_name_plural = "Сообщения чатов"
