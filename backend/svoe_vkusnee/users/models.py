from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Пользователи проекта SvoeVkusnee """

    first_name = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        null=False,
    )
    last_name = models.CharField(
        verbose_name='Фамилия пользователя',
        max_length=150,
        null=False,
    )
    username = models.CharField(
        verbose_name='Ник пользователя',
        max_length=150,
        null=False,
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
        null=False,
    )
    phone_number = models.CharField(
        verbose_name='Номер телефона',
        max_length=20,
        null=False,
    )
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']


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
        ordering = ['user']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'owner'],
                name='unique_follow'
            )
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
