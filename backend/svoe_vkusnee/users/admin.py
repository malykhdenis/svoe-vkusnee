from django.contrib import admin
from django.contrib.auth.models import Group

# Register your models here.
from users.models import User, Follow


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'last_name', 'first_name')
    search_fields = ('username', 'email')
    list_filter = ('first_name', 'last_name')
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'owner')
    empty_value_display = '-пусто-'


admin.site.unregister(Group)
