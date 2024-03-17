from colorfield.fields import ColorField
from django.contrib.auth.models import AbstractUser
from django.core.validators import (MinValueValidator, RegexValidator,
                                    validate_email)
from django.db import models

from .validators import validate_username

MAX_LENGTH_CHARFIELD = 250
MAX_LENGTH_FOR_HEX = 7
MAX_LENGTH_STRING_FOR_USER = 150
MAX_LENGTH_EMAIL = 254


class CustomUser(AbstractUser):
    """Модель пользователя для приложения."""

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=MAX_LENGTH_STRING_FOR_USER,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=MAX_LENGTH_STRING_FOR_USER,
    )
    surname = models.CharField(
        verbose_name='Отчество',
        max_length=MAX_LENGTH_STRING_FOR_USER,
    )
    username = models.CharField(
        verbose_name='Уникальный юзернейм',
        max_length=MAX_LENGTH_STRING_FOR_USER,
        unique=True,
        validators=(
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Имя пользователя содержит недопустимые символы.',
            ),
            validate_username,
        ),
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=MAX_LENGTH_STRING_FOR_USER,
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=MAX_LENGTH_EMAIL,
        unique=True,
        validators=(validate_email,),
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='unique_user_with_email',
            ),
        ]

    def __str__(self):
        return self.username


class Reason(models.Model):
    """Модель поводов для сборов."""

    name = models.CharField(
        verbose_name='Название повода',
        max_length=MAX_LENGTH_CHARFIELD,
    )
    color = ColorField(
        verbose_name='Цвет повода в hex-формате',
        max_length=MAX_LENGTH_FOR_HEX,
        default='#000000',
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=MAX_LENGTH_CHARFIELD,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Повод'
        verbose_name_plural = 'Поводы'

    def __str__(self):
        return self.name


class Collect(models.Model):
    """Модель групповых денежных сборов."""

    author = models.ForeignKey(
        verbose_name='Автор платежа',
        to=CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='collect_author',
    )
    name = models.CharField(
        verbose_name='Название сбора',
        max_length=MAX_LENGTH_CHARFIELD,
    )
    reason = models.ForeignKey(
        verbose_name='Повод для сбора',
        to=Reason,
        on_delete=models.CASCADE,
        related_name='collects',
    )
    description = models.TextField(
        verbose_name='Описание сбора',
    )
    planned_amount = models.PositiveBigIntegerField(
        verbose_name='Планируемая сумма сбора',
        blank=True,
        null=True,
        default=None,
    )
    cover_image = models.ImageField(
        verbose_name='Обложка сбора',
        upload_to='collects/',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата создания сбора',
        auto_now_add=True,
        editable=False,
    )
    end_date = models.DateTimeField(
        verbose_name='Дата окончания сбора',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Сбор'
        verbose_name_plural = 'Сборы'

    def __str__(self):
        return f'{self.author} начал сбор на {self.name}'


class Payment(models.Model):
    """Модель платежа для сборов."""

    user = models.ForeignKey(
        verbose_name='Автор платежа',
        to=CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='payment_author',
    )
    amount = models.PositiveBigIntegerField(
        verbose_name='Сумма платежа',
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Выберете сумму, которую готовы заплатить!',
            ),
        ],
    )
    comments = models.CharField(
        verbose_name='Комментарий к платежу',
        max_length=MAX_LENGTH_CHARFIELD,
    )
    created_at = models.DateTimeField(
        verbose_name='Дата платежа',
        auto_now_add=True,
        editable=False,
    )
    collect = models.ForeignKey(
        verbose_name='Сбор для которого платеж',
        to=Collect,
        on_delete=models.CASCADE,
        related_name='payments',
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return f'{self.user} добавил {self.amount} к {self.collect.name}'
