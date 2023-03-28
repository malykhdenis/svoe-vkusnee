from django.contrib import admin

from .models import (Shop, ShopProduct, Product, Category, Subcategory,
                     FavoriteProduct, FavoriteShop, Messenger)


class ProductInShopAdmin(admin.TabularInline):
    model = ShopProduct
    fields = ('product', 'availability')
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
        'contacts',
        'delivery',
        'logo',
        'count_favorite_shops',)
    list_filter = (
        'name',
        'owner',)
    search_fields = (
        'name',
        'owner__email',
        'categorys__name',
        'subcategorys__name',
        'products__name',)
    # inlines = (ProductInShopAdmin,)
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
    list_display = ('name', 'description')
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
