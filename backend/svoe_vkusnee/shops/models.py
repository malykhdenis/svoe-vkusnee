from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Shop(models.Model):
    """Производители."""
    pass


class Category(models.Model):
    """Категории."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    photo = models.ImageField()


class Subcategory(models.Model):
    """Подкатегории."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,)


class Product(models.Model):
    """Продукты."""
    name = models.CharField(max_length=100)
    photo = models.ImageField()
    description = models.TextField()
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.SET_NULL,
        null=True,
        )


class FavoriteShop(models.Model):
    """Магазин в избранном."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)


class FavoriteProduct(models.Model):
    """Продукт в избранном."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
