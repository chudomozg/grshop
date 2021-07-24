from django.contrib import admin
from .models import Promo


class PromoAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'discount']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Promo, PromoAdmin)
