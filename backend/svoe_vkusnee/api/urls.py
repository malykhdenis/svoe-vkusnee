from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    UserCustomViewSet,
    ShopViewSet,
    ProductViewSet,
    CategoryViewSet,
    SubcategoryViewSet
)

app_name = 'api'

router = DefaultRouter()
router.register('users', UserCustomViewSet, basename='users')
router.register('shops', ShopViewSet, basename='shops')
router.register('products', ProductViewSet, basename='products')
router.register('categorys', CategoryViewSet, basename='categorys')
router.register('subcategorys', SubcategoryViewSet, basename='subcategorys')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]