from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import CheckConstraint, F, Q, UniqueConstraint


class User(AbstractUser):
    """Users of project SvoeVkusnee """

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name', )
    first_name = models.CharField(
        max_length=150,
    )
    last_name = models.CharField(
        max_length=150,
    )
    username = models.CharField(
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        unique=True,
        max_length=254
    )
    password = models.CharField(
        max_length=128,
    )
    phone_number = models.CharField(
        max_length=20,
    )

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ('username', )

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Subscribes."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        verbose_name_plural = 'follows'
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
        return f'{self.user} is subscribed on {self.owner}'
