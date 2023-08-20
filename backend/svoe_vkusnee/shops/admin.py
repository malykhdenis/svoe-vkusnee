from django.contrib import admin
import django.apps

from .models import (Shop, ShopProduct, Product, Category, Subcategory,
                     FavoriteProduct, FavoriteShop, Messenger, ShopMessenger)


admin.site.index_title = 'Svoe vkusnee'
admin.site.site_header = 'SvoeVkusneeAdmin'
admin.site.site_title = 'svoe_vkusnee_admin'


class ProductInShopAdmin(admin.TabularInline):
    model = ShopProduct
    fields = ('product', 'availability')
    classes = ('collapse',)
    extra = 0


class MessengerInShopAdmin(admin.TabularInline):
    model = ShopMessenger
    fields = ('messenger', 'search_information')
    classes = ('collapse',)
    extra = 0


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    fieldsets = (
        ('main', {
            'fields': (
                'name',
                'mainstream',
                'description',
                'owner',
                'history',),
            'description': 'main information about shop'}),
        ('contact information', {
            'fields': (
                'region',
                'city',
                'street',
                'house',
                'coordinates',
                'contacts',
                'presented'),
            'classes': ('collapse',),
            'description': 'shops contacts'}),
        ('other', {
            'fields': (
                'certificate',
                'certificate_photo',
                'delivery',
                'photo',
                'logo',),
            'classes': ('collapse',),
            'description': 'other information'}),
    )
    list_display = (
        'id',
        'get_owner',
        'name',
        'mainstream',
        'city',
        'count_followers',
    )
    list_filter = (
        'city',
        'mainstream',
    )
    search_fields = (
        'name',
        'mainstream',
        'city',
        'categorys__name',
        'subcategorys__name',
        'products__name',
    )
    inlines = (
        ProductInShopAdmin, MessengerInShopAdmin,)
    readonly_fields = ('count_followers',)
    empty_value_display = '-empty-'

    @admin.display(description='owners')
    def get_owner(self, obj):
        return obj.owner.username

    @admin.display(description='categories')
    def get_categories(self, obj):
        return ', '.join([category.name for category in obj.categories.all()])

    @admin.display(description='subcategories')
    def get_subcategories(self, obj):
        return ', '.join(
            [subcategory.name for subcategory in obj.subcategories.all()]
        )

    @admin.display(description='products')
    def get_products(self, obj):
        return ', '.join([
            products.name for products in obj.products.all()])

    @admin.display(description='amount of followers')
    def count_followers(self, obj):
        return obj.followers.count()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    list_filter = ('subcategory',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = (('name', 'slug',), 'photo',)
    list_display = ('id', 'name', 'slug',)
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'category',)
    search_fields = ('name',)
    list_filter = ('category',)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(FavoriteShop)
class FavoriteShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'shop')
    search_fields = ('user', 'shop')
    list_filter = ('user', 'shop')


@admin.register(FavoriteProduct)
class FavoriteProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product')
    search_fields = ('user', 'product')
    list_filter = ('user', 'product')


@admin.register(ShopProduct)
class ShopProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'product', 'availability')
    search_fields = ('shop', 'product')
    list_filter = ('shop', 'product')


@admin.register(Messenger)
class MessengerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)


@admin.register(ShopMessenger)
class ShopMessengerAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'messenger', 'search_information',)
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
