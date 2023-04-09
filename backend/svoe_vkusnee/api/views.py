from django.db import IntegrityError
from djoser.views import UserViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import (
    SAFE_METHODS,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from users.models import Follow, User
from shops.models import (
    Shop, Product, FavoriteProduct, FavoriteShop, Category, Subcategory,
    Messenger
)
from .pagination import Pagination
from .filters import ProductFilter, ShopFilter, MessengerFilter
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    UserCustomSerializer,
    FollowSerializer,
    ProductSerializer,
    ShopCreateSerializer,
    ShopSerializer,
    ShopFieldSerializer,
    SubcategorySerializer,
    CategorySerializer,
    MessengerSerializer,
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
                    {'message': 'Вы уже подписаны на этого производителя'},
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


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение списка товаров."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (ProductFilter,)
    pagination_class = None
    search_fields = ('^name', )
    permission_classes = (IsAuthenticatedOrReadOnly,)


class MessengerViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение списка мессенджеров."""

    queryset = Messenger.objects.all()
    serializer_class = MessengerSerializer
    filter_backends = (MessengerFilter,)
    pagination_class = None
    search_fields = ('^name', )
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение списка категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None


class SubcategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение списка категорий."""

    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None

class ShopViewSet(viewsets.ModelViewSet):
    """Все действия с магазинами."""

    queryset = Shop.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ShopFilter
    pagination_class = Pagination
    permission_classes = (IsAuthorOrReadOnly,)

    def update(self, request, *args, **kwargs):
        if kwargs['partial'] is False:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ShopSerializer
        return ShopCreateSerializer

    def add_to(self, model, user, pk):
        if model.objects.filter(user=user, shop__id=pk).exists():
            return Response({'errors': 'Магазин уже был добавлен.'},
                            status=status.HTTP_400_BAD_REQUEST)
        shop = get_object_or_404(Shop, id=pk)
        model.objects.create(user=user, shop=shop)
        serializer = ShopFieldSerializer(shop)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_from(self, model, user, pk):
        obj = model.objects.filter(user=user, shop__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Магазин уже был удален.'},
            status=status.HTTP_404_NOT_FOUND
        )

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated, )
    )
    def favorited_shops(self, request, **kwargs):
        """Добавление магазина в избранное или удаление из избранного."""
        try:
            shop_id = int(self.kwargs.get('pk'))
        except ValueError:
            return Response(
                {
                    'message': (
                        'Магазин с идентификатором '
                        f'{self.kwargs.get("pk")} не найден'
                    )
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if request.method == 'POST':
            return self.add_to(FavoriteShop, request.user, pk=shop_id)

        if request.method == 'DELETE':
            return self.delete_from(FavoriteShop, request.user, shop_id)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # @action(
    #     detail=True,
    #     methods=('post', 'delete'),
    #     permission_classes=(IsAuthenticated, )
    # )

    # def favorited_products(self, request, **kwargs):
    #     """Добавление товара в избранное или удаление из избранного."""
    #     try:
    #         product_id = int(self.kwargs.get('pk'))
    #     except ValueError:
    #         return Response(
    #             {
    #                 'message': (
    #                     'Товар с идентификатором '
    #                     f'{self.kwargs.get("pk")} не найден'
    #                 )
    #             },
    #             status=status.HTTP_404_NOT_FOUND
    #         )

    #     if request.method == 'POST':
    #         return self.add_to(FavoriteProduct, request.user, pk=product_id)

    #     if request.method == 'DELETE':
    #         return self.delete_from(FavoriteProduct, request.user, product_id)
    #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
