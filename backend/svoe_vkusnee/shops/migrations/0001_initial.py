# Generated by Django 4.1.5 on 2023-04-09 07:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название категории', max_length=200, verbose_name='Название категории')),
                ('slug', models.SlugField(help_text='Введите слаг', max_length=200, unique=True, verbose_name='Слаг')),
                ('photo', models.ImageField(blank=True, help_text='Загрузите картинку', upload_to='shops/images/', verbose_name='Картинка')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='FavoriteProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Избранный продукт',
                'verbose_name_plural': 'Избранные продукты',
                'ordering': ('user',),
            },
        ),
        migrations.CreateModel(
            name='FavoriteShop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Избранный магазин',
                'verbose_name_plural': 'Избранные магазины',
                'ordering': ('user',),
            },
        ),
        migrations.CreateModel(
            name='Messenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название мессенджера', max_length=100, unique=True, verbose_name='Название мессенджера')),
                ('logo', models.ImageField(blank=True, upload_to='shops/images/', verbose_name='Логотип')),
            ],
            options={
                'verbose_name': 'Мессенджер',
                'verbose_name_plural': 'Мессенджеры',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название продукта', max_length=200, verbose_name='Название продута')),
                ('photo', models.ImageField(blank=True, help_text='Загрузите картинку', upload_to='shops/images/', verbose_name='Картинка')),
                ('description', models.TextField(help_text='Введите описание продукта', verbose_name='Описание продукта')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название магазина', max_length=200, unique=True, verbose_name='Название магазина')),
                ('mainstream', models.CharField(default=None, help_text='Введите осносное направление магазина', max_length=200, verbose_name='Основное направление')),
                ('description', models.TextField(default=None, help_text='Введите описание магазина', verbose_name='Описание магазина')),
                ('region', models.CharField(default=None, help_text='Введите регион', max_length=50, verbose_name='Регион')),
                ('city', models.CharField(default=None, help_text='Введите город', max_length=50, verbose_name='Город')),
                ('street', models.CharField(default=None, help_text='Введите название улицы', max_length=50, verbose_name='Улица')),
                ('house', models.CharField(default=None, help_text='Введите номер дома', max_length=10, verbose_name='Номер дома')),
                ('history', models.TextField(default=None, help_text='Введите историю создания магазина', verbose_name='История создания магазина')),
                ('coordinates', models.CharField(default=None, help_text='Введите координаты магазина', max_length=200, verbose_name='Координаты')),
                ('sertificate', models.BooleanField(default=False)),
                ('sertificate_photo', models.ImageField(blank=True, upload_to='shops/images/', verbose_name='Сертификат')),
                ('presented', models.CharField(default=None, help_text='Введите где представлен продукт', max_length=200, verbose_name='Где представлен продукт')),
                ('delivery', models.CharField(default=None, max_length=200, verbose_name='Доставка')),
                ('contacts', models.CharField(default=None, max_length=200, verbose_name='Контактная информация')),
                ('photo', models.ImageField(blank=True, upload_to='shops/images/', verbose_name='Фотография')),
                ('logo', models.ImageField(blank=True, upload_to='shops/images/', verbose_name='Логотип')),
            ],
            options={
                'verbose_name': 'Магазин',
                'verbose_name_plural': 'Магазины',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название подкатегории', max_length=200, verbose_name='Название подкатегории')),
                ('slug', models.SlugField(help_text='Введите слаг', max_length=200, unique=True, verbose_name='Слаг')),
                ('category', models.ForeignKey(help_text='Категория', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subcategory', to='shops.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Подкатегория',
                'verbose_name_plural': 'Подкатегории',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ShopProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('availability', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_products', to='shops.product', verbose_name='Продукт')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_products', to='shops.shop', verbose_name='Магазин')),
            ],
            options={
                'verbose_name': 'Продукт магазина',
                'verbose_name_plural': 'Продукты магазина',
            },
        ),
        migrations.CreateModel(
            name='ShopMessenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_information', models.CharField(help_text='Введите логин мессенджера', max_length=100, unique=True, verbose_name='Логин мессенджера')),
                ('messenger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_messengers', to='shops.messenger', verbose_name='Месенджер')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_messengers', to='shops.shop', verbose_name='Магазин')),
            ],
            options={
                'verbose_name': 'Мессенджер магазина',
                'verbose_name_plural': 'Мессенджеры магазина',
            },
        ),
        migrations.AddField(
            model_name='shop',
            name='messengers',
            field=models.ManyToManyField(blank=True, help_text='Выберите мессенджер', related_name='shops', through='shops.ShopMessenger', to='shops.messenger', verbose_name='Мессенджеры'),
        ),
    ]
