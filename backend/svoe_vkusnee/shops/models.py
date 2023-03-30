from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    """Категории."""
    name = models.CharField(
        verbose_name='Название категории',
        max_length=200,
        help_text='Введите название категории',
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=200,
        unique=True,
        help_text='Введите слаг'
    )
    photo = models.ImageField(
        verbose_name='Картинка',
        upload_to='images/categories/',
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
        help_text='Введите название подкатегории',
        blank=False,
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
        related_name='subcategories',
        help_text='Выберите категорию'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

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
        upload_to='images/products/',
        blank=True,
        help_text='Загрузите картинку'
    )
    description = models.TextField(
        verbose_name='Описание продукта',
        help_text='Введите описание продукта'
    )
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Подкатегория',
        related_name='products',
        help_text='Выберите подкатегорию'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class Messenger(models.Model):
    """Мессенджеры."""
    name = models.CharField(
        verbose_name='Название мессенджера',
        max_length=100,
        help_text='Введите название мессенджера',
        unique=True,
    )
    logo = models.ImageField(
        verbose_name='Логотип',
        upload_to='images/messengers/',
        blank=True,
    )

    class Meta:
        verbose_name = 'Мессенджер'
        verbose_name_plural = 'Мессенджеры'

    def __str__(self):
        return self.name


class Shop(models.Model):
    """Магазины производителей."""

    MAINSTREAMS = [
        ('M_1', 'MAINSTREAM_1'),
        ('M_2', 'MAINSTREAM_2'),
        ('M_3', 'MAINSTREAM_3'),
        ('M_4', 'MAINSTREAM_4'),
        ('M_5', 'MAINSTREAM_5'),
    ]

    name = models.CharField(
        verbose_name='Название магазина',
        max_length=200,
        help_text='Введите название магазина',
        unique=True,
    )
    mainstream = models.CharField(
        verbose_name='Основное направление',
        max_length=3,
        help_text='Выберите основное направление магазина',
        choices=MAINSTREAMS,
        blank=True,
    )
    description = models.TextField(
        verbose_name='Описание магазина',
        help_text='Введите описание магазина',
        blank=True,
    )
    region = models.CharField(
        verbose_name='Регион',
        max_length=50,
        help_text='Введите регион',
        blank=True,
    )
    city = models.CharField(
        verbose_name='Город',
        max_length=50,
        help_text='Введите город',
        blank=True,
    )
    street = models.CharField(
        verbose_name='Улица',
        max_length=50,
        help_text='Введите название улицы',
        blank=True,
    )
    house = models.CharField(
        verbose_name='Номер дома',
        max_length=10,
        help_text='Введите номер дома',
        blank=True,
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name='Собственник',
        related_name='shops',
        help_text='Выберите собственника',
        default=None,
        blank=True,
        null=True,
    )
    history = models.TextField(
        verbose_name='История создания магазина',
        help_text='Введите историю создания магазина',
        blank=True,
    )
    coordinates = models.CharField(
        verbose_name='Координаты',
        max_length=200,
        help_text='Введите координаты магазина',
        blank=True,
    )
    certificate = models.BooleanField(
        default=False,
        verbose_name='Наличие сертификата',
    )
    certificate_photo = models.ImageField(
        verbose_name='Сертификат',
        upload_to='images/certificates/',
        blank=True,
    )
    presented = models.TextField(
        verbose_name='Где представлен продукт',
        help_text='Введите где представлен продукт',
        blank=True,
    )
    delivery = models.BooleanField(
        default=False,
        verbose_name='Наличие доставки',
    )
    contacts = models.CharField(
        verbose_name='Контактная информация',
        max_length=200,
        blank=True,
    )
    photo = models.ImageField(
        verbose_name='Фотография',
        upload_to='images/shops/',
        blank=True,
    )
    logo = models.ImageField(
        verbose_name='Логотип',
        upload_to='images/shops_logos/',
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
    messengers = models.ManyToManyField(
        Messenger,
        blank=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return self.name


class ShopProduct(models.Model):
    """Товары магазина"""
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name='product',
        verbose_name='Магазин',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='shop',
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

    def __str__(self):
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
        related_name='followers'
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
        related_name='favorite_products',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='followers'
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
