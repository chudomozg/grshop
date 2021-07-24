from django.contrib import admin
from .models import Category, Product, Promo


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'price', 'stock', 'available']
    list_filter = ['available', 'price', 'stock']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Product, ProductAdmin)


class PromoAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'discount']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Promo, PromoAdmin)
