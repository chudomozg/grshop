from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from .models import Promo, ProductGroupDiscount, SimpleDiscount, CountInStock


class PromoChildAdmin(PolymorphicChildModelAdmin):
    """ Base admin class for all child models """
    base_model = Promo  # Optional, explicitly set here.

    # By using these `base_...` attributes instead of the regular ModelAdmin `form` and `fieldsets`,
    # the additional fields of the child models are automatically added to the admin form.
    # base_form = ...
    # base_fieldsets = ['title', 'promo_code', 'slug', 'discount', 'start_date', 'end_date']


@admin.register(ProductGroupDiscount)
class ProductGroupDiscountAdmin(PromoChildAdmin):
    base_model = ProductGroupDiscount
    prepopulated_fields = {'slug': ('title',)}


@admin.register(SimpleDiscount)
class SimpleDiscountAdmin(PromoChildAdmin):
    base_model = SimpleDiscount
    prepopulated_fields = {'slug': ('title',)}


@admin.register(CountInStock)
class CountInStockAdmin(PromoChildAdmin):
    base_model = CountInStock
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Promo)
class PromoParentAdmin(PolymorphicParentModelAdmin):
    """ The parent model admin """
    base_model = Promo  # Optional, explicitly set here.
    child_models = (ProductGroupDiscount, SimpleDiscount, CountInStock)
    base_fieldsets = ['title', 'promo_code', 'slug', 'discount', 'start_date', 'end_date']
    list_filter = (PolymorphicChildModelFilter,)  # This is optional.
