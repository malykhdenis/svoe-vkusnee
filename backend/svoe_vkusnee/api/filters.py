import django_filters
from rest_framework.filters import SearchFilter

from shops.models import Shop, Product, Category, Subcategory, Messenger


class ProductFilter(SearchFilter):
    search_param = 'name'

    class Meta:
        model = Product
        fields = ('name', )


class MessengerFilter(SearchFilter):
    search_param = 'name'

    class Meta:
        model = Messenger
        fields = ('name', )


class ShopFilter(django_filters.FilterSet):
    # categorys = django_filters.ModelMultipleChoiceFilter(
    #     field_name='categorys__slug',
    #     to_field_name='slug',
    #     queryset=Category.objects.all()
    # )
    # subcategorys = django_filters.ModelMultipleChoiceFilter(
    #     field_name='subcategorys__slug',
    #     to_field_name='slug',
    #     queryset=Subcategory.objects.all()
    # )
    is_favorited_shops = django_filters.NumberFilter(
        method='filter_is_favorited_shops',
    )
    # is_favorited_products = django_filters.NumberFilter(
    #     method='filter_is_favorited_products',
    # )

    class Meta:
        model = Shop
        fields = ('owner', 'is_favorited_shops', )

    def filter_is_favorited_shops(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(favorite_shops__user=self.request.user)
        return queryset

    # def filter_is_favorited_products(self, queryset, name, value):
    #     user = self.request.user
    #     if value and not user.is_anonymous:
    #         return queryset.filter(favorite_products__user=self.request.user)
    #     return queryset
