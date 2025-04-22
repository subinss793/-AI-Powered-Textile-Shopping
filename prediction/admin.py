from django.contrib import admin

from .models import UserProfile
from .models import Category, Dress

# Register your models here.
admin.site.register(UserProfile)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Dress)
class DressAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price')
    list_filter = ('category',)

