from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from users.models import (Follow,
                          User,)
from shops.models import (Shop,
                          Category,
                          Subcategory,
                          Product,
                          ShopProduct,
                          FavoriteShop,
                          FavoriteProduct)
from drf_extra_fields.fields import Base64ImageField


class UserCustomCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователя"""
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'id',
            'email',
            'username',
            'password',
            'first_name',
            'last_name',
            'phone_number'
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Недопустимое имя пользователя')
        return value


class UserCustomSerializer(UserSerializer):
    """Сериализатор для получения данных пользователя"""
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'phone_number',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, owner=obj).exists()


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок"""
    email = serializers.EmailField(source='owner.email')
    id = serializers.IntegerField(source='owner.id')
    username = serializers.CharField(source='owner.username')
    first_name = serializers.CharField(source='owner.first_name')
    last_name = serializers.CharField(source='owner.last_name')
    phone_number = serializers.CharField(source='owner.phone_number')
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    shops = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'phone_number',
            'is_subscribed'
            'shops'
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        owner = obj.owner
        if user.is_authenticated:
            return Follow.objects.filter(user=user, owner=owner).exists()
        return False

    def get_shops(self, obj):
        request = self.context.get('request')
        shops = Shop.objects.filter(owner=obj.owner)
        limit = request.GET.get('shops_limit')
        if limit:
            shops = shops[:int(limit)]
        return ShopFieldSerializer(
            shops,
            many=True,
            context={'request': request}
        ).data

    def get_shops_count(self, obj):
        return Shop.objects.filter(owner=obj.owner).count()


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для товаров."""

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'photo',
            'description',
            'subcategory'
        )


class SubcategorySerializer(serializers.ModelSerializer):
    """Сериализатор для субкатегории."""

    class Meta:
        model = Subcategory
        fields = (
            'id',
            'name',
            'category',
            'slug'
        )


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категории."""

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'photo',
            'slug'
        )


class ShopProductSerializer(serializers.ModelSerializer):
    """Сериализатор для товаров магазина."""

    id = serializers.IntegerField(source='product.id')
    name = serializers.CharField(source='product.name')

    class Meta:
        model = ShopProduct
        fields = (
            'id',
            'name',
            'availability'
        )


# class ProductFieldSerializer(serializers.ModelSerializer):
#     """Сериализатор для введения полей продукта при создании магазина."""

#     id = serializers.PrimaryKeyRelatedField(
#         queryset=Product.objects.all(),
#     )
#     availability = serializers.BooleanField()

#     class Meta:
#         model = ShopProduct
#         fields = ('id', 'availability')


class ShopSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра магазинов."""

    category = CategorySerializer(many=True, read_only=True)
    subcategory = SubcategorySerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True, many=False)
    products = serializers.SerializerMethodField()
    # is_favorited_shops = serializers.SerializerMethodField()
    # is_favorited_products = serializers.SerializerMethodField()
    photo = Base64ImageField()

    class Meta:
        model = Shop
        fields = (
            'id',
            'owner',
            'name',
            'photo',
            'mainstream',
            'description',
            'history',
            'coordinates',
            'sertificate',
            'sertificate_photo',
            'presented',
            'delivery',
            'contacts',
            'logo',
            'products',
            'category',
            'subcategory',
            # 'is_favorited_shops',
            # 'is_favorited_products',
            'messengers',
        )

    def get_products(self, obj):
        products = ShopProduct.objects.filter(shop=obj)
        return ShopProductSerializer(products, many=True).data

    def get_is_favorited_shops(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorites.filter(shop=obj).exists()

    def get_is_favorited_products(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorites.filter(product=obj).exists()


class ShopCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания магазина."""

    # category = serializers.PrimaryKeyRelatedField(
    #     queryset=Category.objects.all(), many=True
    # )
    # subcategory = serializers.PrimaryKeyRelatedField(
    #     queryset=Subcategory.objects.all(), many=True
    # )
    # products = ProductFieldSerializer(many=True)
    owner = UserCustomSerializer(read_only=True)
    # photo = Base64ImageField()

    class Meta:
        model = Shop
        fields = (
            'id',
            'owner',
            'name',
            # 'photo',
            'mainstream',
            'description',
            # 'adress',
            'history',
            'coordinates',
            'city',
            'house',
            'region',
            'street',
            'sertificate',
            'sertificate_photo',
            'presented',
            'delivery',
            'contacts',
            'logo',
            # 'products',
            # 'categorys',
            # 'subcategorys',
            'messengers',
        )

    # def validate(self, data):
    #     """Проверка наличия товаров, субкатегорий, категорий."""
    #     products = self.initial_data.get('products')
    #     if not products:
    #         raise serializers.ValidationError({
    #             'products': 'Необходимо выбрать товар.'
    #         })

    #     products_id = [product['id'] for product in products]
    #     if len(products_id) != len(set(products_id)):
    #         raise serializers.ValidationError({
    #             'products': 'товары не должны повторяться.'
    #         })

    #     categorys = self.initial_data.get('categorys')
    #     if not categorys:
    #         raise serializers.ValidationError({
    #             'categorys': 'Необходимо выбрать категорию.'
    #         })

    #     subcategorys = self.initial_data.get('subcategorys')
    #     if not subcategorys:
    #         raise serializers.ValidationError({
    #             'subcategorys': 'Необходимо выбрать субкатегорию.'
    #         })

    #     return data

    def create_products(self, products, shop):
        """Создание товара."""
        for product in products:
            product_id = product['id']
            availability = product['availability']
            ShopProduct.objects.create(
                shop=shop, product=product_id, availability=availability
            )

    def create_categorys(self, categorys, shop):
        """Создание категорий"""
        for category in categorys:
            shop.categorys.add(category)

    def create_subcategorys(self, subcategorys, shop):
        """Создание субкатегорий"""
        for subcategory in subcategorys:
            shop.subcategorys.add(subcategory)

    def create(self, validated_data):
        """Создание магазина."""
        owner = self.context.get('request').user
        # categorys = validated_data.pop('categorys')
        # subcategorys = validated_data.pop('subcategorys')
        # products = validated_data.pop('products')
        shop = Shop.objects.create(owner=owner, **validated_data)
        # self.create_categorys(categorys, shop)
        # self.create_subcategorys(subcategorys, shop)
        # self.create_products(products, shop)
        return shop

    def update(self, instance, validated_data):
        """Обновление магазина."""
        instance.photo = validated_data.get('photo', instance.photo)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.mainstream = validated_data.get(
            'mainstream', instance.mainstream)
        instance.adress = validated_data.get('adress', instance.adress)
        instance.history = validated_data.get('history', instance.history)
        instance.coordinates = validated_data.get(
            'coordinates', instance.coordinates)
        instance.sertificate = validated_data.get(
            'sertificate', instance.sertificate)
        instance.sertificate_photo = validated_data.get(
            'sertificate_photo', instance.sertificate_photo)
        instance.presented = validated_data.get(
            'presented', instance.presented)
        instance.delivery = validated_data.get(
            'delivery', instance.delivery)
        instance.contacts = validated_data.get(
            'contacts', instance.contacts)
        instance.logo = validated_data.get('logo', instance.logo)

        instance.categorys.clear()
        categorys = validated_data.get('categorys')
        self.create_categorys(categorys, instance)

        instance.subcategorys.clear()
        subcategorys = validated_data.get('subcategorys')
        self.create_subcategorys(subcategorys, instance)

        ShopProduct.objects.filter(shop=instance).all().delete()
        products = validated_data.get('products')
        self.create_products(products, instance)

        instance.save()
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShopSerializer(
            instance, context=context).data


class ShopFieldSerializer(serializers.ModelSerializer):
    """Сериализатор для получения полей магазина."""

    class Meta:
        model = Shop
        fields = (
            'id',
            'name',
            'photo',
            'mainstream',
            'products',
        )


class ProductFieldSerializer(serializers.ModelSerializer):
    """Сериализатор для получения полей товара."""

    class Meta:
        model = Shop
        fields = (
            'id',
            'name',
            'photo',
            'category',
        )


class FavoriteShopSerializer(serializers.ModelSerializer):
    """Сериализатор для избранных магазинов."""

    class Meta:
        model = FavoriteShop
        fields = ('user', 'shop')

    def to_representation(self, instance):
        """Получение избранных магазинов."""
        return ShopFieldSerializer(
            instance.shop,
            context={'request': self.context.get('request')}
        ).data


class FavoriteProductSerializer(serializers.ModelSerializer):
    """Сериализатор для избранных товаров."""

    class Meta:
        model = FavoriteProduct
        fields = ('user', 'product')

    def to_representation(self, instance):
        """Получение избранных магазинов."""
        return ProductFieldSerializer(
            instance.product,
            context={'request': self.context.get('request')}
        ).data
