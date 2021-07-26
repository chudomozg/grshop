from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from promo.models import Promo
from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'price', 'stock', 'available']
    list_filter = ['available', 'price', 'stock']
    list_editable = ['price', 'stock', 'available']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Product, ProductAdmin)