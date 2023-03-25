from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    """Категории."""
    name = models.CharField(
        verbose_name='Название категории',
        max_length=200,
        help_text='Введите название категории'
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=200,
        unique=True,
        help_text='Введите слаг'
    )
    photo = models.ImageField(
        verbose_name='Картинка',
        upload_to='shops/images/',
        blank=True,
        help_text='Загрузите картинку'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    """Подкатегории."""
    name = models.CharField(
        verbose_name='Название подкатегории',
        max_length=200,
        help_text='Введите название подкатегории'
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=200,
        unique=True,
        help_text='Введите слаг'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='subcategory',
        help_text='Категория'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Субкатегория'
        verbose_name_plural = 'Субкатегории'

    def __str__(self):
        return self.name


class Product(models.Model):
    """Продукты."""
    name = models.CharField(
        verbose_name='Название продута',
        max_length=200,
        help_text='Введите название продукта'
    )
    photo = models.ImageField(
        verbose_name='Картинка',
        upload_to='shops/images/',
        blank=True,
        help_text='Загрузите картинку'
    )
    description = models.TextField(
        verbose_name='Описание продукта',
        help_text='Введите описание продукта'
    )
    # shop = models.ForeignKey(
    #     Shop,
    #     on_delete=models.CASCADE
    # )
    subcategory = models.ManyToManyField(
        Subcategory,
        verbose_name='Подкатегория',
        related_name='Подкатегории',
        help_text='Выберите подкатегорию'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class Shop(models.Model):
    """Магазины производителей."""
    name = models.CharField(
        verbose_name='Название магазина',
        max_length=200,
        help_text='Введите название магазина',
        default=None
    )
    mainstream = models.CharField(
        verbose_name='Основное направление',
        max_length=200,
        help_text='Введите осносное направление магазина',
        default=None
    )
    description = models.TextField(
        verbose_name='Описание магазина',
        help_text='Введите описание магазина',
        default=None
    )
    adress = models.CharField(
        verbose_name='Адрес',
        max_length=200,
        help_text='Введите адрес магазина',
        default=None
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Производитель',
        related_name='shops',
        help_text='Производитель',
        default=None
    )
    history = models.TextField(
        verbose_name='История создания магазина',
        help_text='Введите историю создания магазина',
        default=None
    )
    coordinates = models.CharField(
        verbose_name='Координаты',
        max_length=200,
        help_text='Введите координаты магазина',
        default=None
    )
    sertificate = models.BooleanField(default=False)
    sertificate_photo = models.ImageField(
        verbose_name='Сертификат',
        upload_to='shops/images/',
        blank=True,
    )
    presented = models.CharField(
        verbose_name='Где представлен продукт',
        max_length=200,
        help_text='Введите где представлен продукт',
        default=None
    )
    delivery = models.CharField(
        verbose_name='Доставка',
        max_length=200,
        default=None
    )
    contacts = models.CharField(
        verbose_name='Контактная информация',
        max_length=200,
        default=None
    )
    photo = models.ImageField(
        verbose_name='Фотография',
        upload_to='shops/images/',
        blank=True,
    )
    logo = models.ImageField(
        verbose_name='Логотип',
        upload_to='shops/images/',
        blank=True,
    )
    products = models.ManyToManyField(
        Product,
        through='ShopProduct',
        through_fields=('shop', 'product'),
        verbose_name='Продукты',
        related_name='shops',
        blank=True,
        help_text='Выберите продукты'
    )
    categorys = models.ManyToManyField(
        Category,
        verbose_name='Категории',
        related_name='магазины',
        help_text='Выберите категории'
    )
    subcategorys = models.ManyToManyField(
        Subcategory,
        verbose_name='Подкатегории',
        related_name='магазины',
        help_text='Выберите подкатегории'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self) -> str:
        return self.name


class ShopProduct(models.Model):
    """Товары магазина"""
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name='shop_products',
        verbose_name='Магазин',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='shop_products',
        verbose_name='Продукт',
    )
    availability = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Продукт магазина'
        verbose_name_plural = 'Продукты магазина'
        constraints = [
            models.UniqueConstraint(
                fields=['shop', 'product'],
                name='unique_shop_product'
            )
        ]

    def __str__(self) -> str:
        return f'{self.product} - {self.availability}'


class FavoriteShop(models.Model):
    """Магазин в избранном."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_shops'
    )
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name='favorite_shops'
    )

    class Meta:
        ordering = ('user',)
        verbose_name = 'Избранный магазин'
        verbose_name_plural = 'Избранные магазины'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'shop'],
                name='unique_favorite_shop'
            )
        ]

    def __str__(self) -> str:
        return f'{self.user} - {self.shop}'


class FavoriteProduct(models.Model):
    """Продукт в избранном."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_products'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='favorite_products'
    )

    class Meta:
        ordering = ('user',)
        verbose_name = 'Избранный продукт'
        verbose_name_plural = 'Избранные продукты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'product'],
                name='unique_favorite_product'
            )
        ]

    def __str__(self) -> str:
        return f'{self.user} - {self.product}'
