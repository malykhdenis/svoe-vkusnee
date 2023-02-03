from rest_framework import viewsets
from djoser.views import UserViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from users.models import Follow, User


from .serializers import (
    UserCreateSerializer,
    UserSerializer,
    FollowSerializer,
)

from .permissions import IsAuthor



class UserViewSet(UserViewSet):
    """Создание и получение данных пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

 
    @action(detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated])
    def subscribe(self, request, id):
        """Подписка на производителя"""
        owner = get_object_or_404(User, id=id)
        user = request.user
        
        if request.method == 'POST':
            serializer = FollowSerializer(
                owner,
                data=request.data,
                context={'request': request},
            )
            Follow.objects.get_or_create(user=user, owner=owner)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        if request.method == 'DELETE':
            get_object_or_404(Follow, user=user, owner=owner).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


    def subscriptions(self, request):
        """Получение списка подписок"""
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
