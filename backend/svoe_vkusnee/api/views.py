from django.db import IntegrityError
from rest_framework import viewsets
from djoser.views import UserViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from users.models import Follow, User
from .pagination import Pagination

from .serializers import (
    UserCustomCreateSerializer,
    UserCustomSerializer,
    FollowSerializer,
)


class UserCustomViewSet(UserViewSet):
    """Создание и получение данных пользователя"""
    queryset = User.objects.all()
    serializer_class = UserCustomSerializer
    pagination_class = Pagination

 
    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated, ),
        serializer_class=FollowSerializer,
    )
    def subscribe(self, request, id):
        """Подписка на производителя"""
        owner = self.get_object()
        user = self.request.user

        if user == owner:
            return Response(
                {'message': 'Нельзя подписаться на самого себя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if request.method == 'POST':
            try:
                subscribtion = Follow.objects.create(user=user, owner=owner)
            except IntegrityError:
                return Response(
                    {'message': 'Вы уже подписаны на этого автора'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = self.get_serializer(
                subscribtion,
                context={'request': request},
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            get_object_or_404(Follow, user=user, owner=owner).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, permission_classes=(IsAuthenticated, ))
    def subscriptions(self, request):
        """Получение списка подписок"""
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
