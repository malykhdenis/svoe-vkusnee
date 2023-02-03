from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers, status
from users.models import Follow, User

from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField


class UserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователя"""
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email', 'username', 'password', 'first_name', 'last_name', 'phone_number')


class UserSerializer(UserSerializer):
    """Сериализатор для получения данных пользователя"""
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'phone_number')
    
    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None:
            return False
        return Follow.objects.filter(user=request.user, author=obj).exists()


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок"""
    shops = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'username', 'first_name', 'last_name', 'shops')
        read_only_fields = ('username', 'first_name', 'last_name', 'email')
    
    def validate(self, attrs):
        user = self.context.get('request').user
        owner_id = self.context.get('kwargs').get('pk')
        owner = get_object_or_404(User, id=owner_id)
        if user == owner:
            raise serializers.ValidationError(
                detail='Вы не можете подписаться на себя',
                code=status.HTTP_400_BAD_REQUEST,
            )
        if Follow.objects.filter(user=user, owner=owner).exists():
            raise serializers.ValidationError(
                detail='Вы уже подписаны на этого производителя',
                code=status.HTTP_400_BAD_REQUEST,
            )        
    
    def get_recipes_count(self, obj):
        return obj.recipes.count()
