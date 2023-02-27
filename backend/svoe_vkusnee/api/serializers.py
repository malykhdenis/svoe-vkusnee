from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers, status
from users.models import Follow, User

from django.shortcuts import get_object_or_404
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
    # shops = serializers.SerializerMethodField()

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
            # 'shops'
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        owner = obj.owner
        if user.is_authenticated:
            return Follow.objects.filter(user=user, owner=owner).exists()
        return False

    # def get_shops(self, obj):
    #     request = self.context.get('request')
    #     recipes = Shops.objects.filter(owner=obj.owner)
        # if limit:
        #     recipes = recipes[:int(limit)]
    #     return ShopFieldSerializer(
    #         shops,
    #         many=True,
    #         context={'request': request}
    #     ).data

    # def get_shops_count(self, obj):
    #     return Shop.objects.filter(owner=obj.owner).count()
