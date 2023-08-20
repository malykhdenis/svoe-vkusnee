from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    """Categories."""
    name = models.CharField(
        max_length=200,
        help_text='enter category name',
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        help_text='enter slug'
    )
    photo = models.ImageField(
        upload_to='images/categories/',
        blank=True,
        help_text='download photo'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    """Subcategories."""
    name = models.CharField(
        max_length=200,
        help_text='enter subcategory name',
        blank=False,
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        help_text='enter slug'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='subcategories',
        help_text='choose category'
    )

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'subcategories'

    def __str__(self):
        return self.name


class Product(models.Model):
    """Products."""
    name = models.CharField(
        max_length=200,
        help_text='enter product name'
    )
    photo = models.ImageField(
        upload_to='images/products/',
        blank=True,
        help_text='download photo'
    )
    description = models.TextField(
        help_text='enter description of product'
    )
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products',
        help_text='choose subcategory'
    )

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name


class Messenger(models.Model):
    """Messengers."""
    name = models.CharField(
        max_length=100,
        help_text='enter name of messanger',
        unique=True,
    )
    logo = models.ImageField(
        upload_to='images/messengers/',
        blank=True,
    )

    class Meta:
        verbose_name_plural = 'messengers'

    def __str__(self):
        return self.name


class Shop(models.Model):
    """Shops."""

    MAINSTREAMS = [
        ('M_1', 'MAINSTREAM_1'),
        ('M_2', 'MAINSTREAM_2'),
        ('M_3', 'MAINSTREAM_3'),
        ('M_4', 'MAINSTREAM_4'),
        ('M_5', 'MAINSTREAM_5'),
    ]

    name = models.CharField(
        max_length=200,
        help_text='enter name of shop',
        unique=True,
    )
    mainstream = models.CharField(
        max_length=3,
        help_text='choose mainstream of shop',
        choices=MAINSTREAMS,
        blank=True,
    )
    description = models.TextField(
        help_text='enter description of shop',
        blank=True,
    )
    region = models.CharField(
        max_length=50,
        help_text='enter region',
        blank=True,
    )
    city = models.CharField(
        max_length=50,
        help_text='enter city',
        blank=True,
    )
    street = models.CharField(
        max_length=50,
        help_text='enter street',
        blank=True,
    )
    house = models.CharField(
        max_length=10,
        help_text='enter number of house',
        blank=True,
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='shops',
        help_text='choose an owner',
        default=None,
        blank=True,
        null=True,
    )
    history = models.TextField(
        help_text="enter history of shop' creation",
        blank=True,
    )
    coordinates = models.CharField(
        max_length=200,
        help_text='enter coordinates of shop',
        blank=True,
    )
    certificate = models.BooleanField(
        default=False,
        help_text='availability of a certificate',
    )
    certificate_photo = models.ImageField(
        verbose_name='certificate photo',
        upload_to='images/certificates/',
        blank=True,
    )
    presented = models.TextField(
        help_text='where the product is presented',
        blank=True,
    )
    delivery = models.BooleanField(
        default=False,
        help_text='availability of delivery',
    )
    contacts = models.CharField(
        max_length=200,
        help_text='contact information',
        blank=True,
    )
    photo = models.ImageField(
        upload_to='images/shops/',
        help_text='choose a photo of the product',
        blank=True,
    )
    logo = models.ImageField(
        upload_to='images/shops_logos/',
        help_text='choose a logo',
        blank=True,
    )
    products = models.ManyToManyField(
        Product,
        through='ShopProduct',
        through_fields=('shop', 'product'),
        related_name='shops',
        blank=True,
        help_text='choose products'
    )
    messengers = models.ManyToManyField(
        Messenger,
        through='ShopMessenger',
        through_fields=('shop', 'messenger'),
        related_name='shops',
        blank=True,
        help_text='choose messenger'
    )

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'shops'

    def __str__(self):
        return self.name


class ShopMessenger(models.Model):
    """Shop' messengers."""
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name='related_to_messenger',
    )
    messenger = models.ForeignKey(
        Messenger,
        on_delete=models.CASCADE,
        related_name='related_to_shop',
    )
    search_information = models.CharField(
        max_length=100,
        help_text='enter login',
        unique=True,
    )

    class Meta:
        verbose_name = "shop' messenger"
        verbose_name_plural = "shop' messengers"
        constraints = [
            models.UniqueConstraint(
                fields=['shop', 'messenger'],
                name='unique_messenger_product'
            )
        ]

    def __str__(self):
        return f'{self.shop.name} в {self.messenger}'


class ShopProduct(models.Model):
    """Shop' product."""
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name='product',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='shop',
    )
    availability = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Shop' product"
        verbose_name_plural = "Shop' products"
        constraints = [
            models.UniqueConstraint(
                fields=['shop', 'product'],
                name='unique_shop_product'
            )
        ]

    def __str__(self):
        return f'{self.product} - {self.availability}'


class FavoriteShop(models.Model):
    """Favorite shop."""
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
        verbose_name = 'favorite shop'
        verbose_name_plural = 'favorite shops'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'shop'],
                name='unique_favorite_shop'
            )
        ]

    def __str__(self) -> str:
        return f'{self.user} - {self.shop}'


class FavoriteProduct(models.Model):
    """Favorite product."""
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
        verbose_name = 'favorite product'
        verbose_name_plural = 'favorite products'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'product'],
                name='unique_favorite_product'
            )
        ]

    def __str__(self) -> str:
        return f'{self.user} - {self.product}'
