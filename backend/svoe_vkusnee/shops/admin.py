from django.contrib import admin
import django.apps

from .models import (Shop, ShopProduct, Product, Category, Subcategory,
                     FavoriteProduct, FavoriteShop, Messenger, ShopMessenger)


admin.site.index_title = 'Свое вкуснее'
admin.site.site_header = 'SvoeVkusneeAdmin'
admin.site.site_title = 'svoe_vkusnee_admin'


class ProductInShopAdmin(admin.TabularInline):
    model = ShopProduct
    fields = ('product', 'availability')
    min_num = 1
    extra = 0


class MessengerInShopAdmin(admin.TabularInline):
    model = ShopMessenger
    fields = ('messenger', 'search_information')
    min_num = 1
    extra = 0


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'get_owner',
        'name',
        'description',
        'get_products',
        'get_messengers',
        'contacts',
        'delivery',
        'logo',
        # 'count_favorite_shops',
    )
    list_filter = (
        'name',
        'owner',)
    search_fields = (
        'name',
        'owner__email',
        'categorys__name',
        'subcategorys__name',
        'products__name',
        'messengers__name',
    )
    inlines = (
        ProductInShopAdmin, MessengerInShopAdmin,)
    # inlines = (MessengerInShopAdmin,)
    readonly_fields = ('count_favorite_shops',)
    empty_value_display = '-пусто-'

    @admin.display(description='Собственники')
    def get_owner(self, obj):
        return obj.owner.username

    @admin.display(description='Категории')
    def get_categorys(self, obj):
        return ', '.join([category.name for category in obj.categorys.all()])

    @admin.display(description='Субкатегории')
    def get_subcategorys(self, obj):
        return ', '.join(
            [subcategory.name for subcategory in obj.subcategorys.all()]
        )

    @admin.display(description='Товары')
    def get_products(self, obj):
        return ', '.join([
            products.name for products in obj.products.all()])

    @admin.display(description='Количество избранных магазинов')
    def count_favorite_shops(self, obj):
        return obj.favorite_shops.count()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'photo', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category',)
    search_fields = ('name',)
    list_filter = ('category',)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(FavoriteShop)
class FavoriteShopAdmin(admin.ModelAdmin):
    list_display = ('user', 'shop')
    search_fields = ('user', 'shop')
    list_filter = ('user', 'shop')


@admin.register(FavoriteProduct)
class FavoriteProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    search_fields = ('user', 'product')
    list_filter = ('user', 'product')


@admin.register(ShopProduct)
class ShopProductAdmin(admin.ModelAdmin):
    list_display = (
        'shop', 'product', 'availability'
    )
    search_fields = ('shop', 'product')
    list_filter = ('shop', 'product')


@admin.register(Messenger)
class MessengerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(ShopMessenger)
class ShopMessengerAdmin(admin.ModelAdmin):
    list_display = ('shop', 'messenger', 'search_information',)
    search_fields = ('shop', 'messenger')
    list_filter = ('shop', 'messenger')


def all_models_admin():
    """Регистрирует в admin все модели проекта."""
    models = django.apps.apps.get_models()
    for model in models:
        try:
            admin.site.register(model)
        except admin.sites.AlreadyRegistered:
            pass


# uncomment to show all models in admin
# all_models_admin()
