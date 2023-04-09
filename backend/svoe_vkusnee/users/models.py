from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import CheckConstraint, F, Q, UniqueConstraint


class User(AbstractUser):
    """Пользователи проекта SvoeVkusnee """

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name', )
    first_name = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name='Фамилия пользователя',
        max_length=150,
    )
    username = models.CharField(
        verbose_name='Ник пользователя',
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True,
        max_length=254
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=128,
    )
    phone_number = models.CharField(
        verbose_name='Номер телефона',
        max_length=20,
    )
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username', )


    def __str__(self):
        return self.username

    
class Follow(models.Model):
    """Подписки на производителей."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь',
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Производитель',
    )
    
    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('user', )
        constraints = [
            UniqueConstraint(
                fields=['user', 'owner'],
                name='unique_follow'
            ),
            CheckConstraint(
                check=~Q(user=F('owner')),
                name='no_self_follow'
            )
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.owner}'
