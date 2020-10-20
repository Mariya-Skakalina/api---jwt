from django.contrib import admin
from .models import Post, User, City


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('name',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ('name',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
	list_display = ('name',)
