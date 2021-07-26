from datetime import datetime, timedelta
from django.db import models
from django.urls import reverse
from main.models import Product
from polymorphic.models import PolymorphicModel
from django.utils.crypto import get_random_string


class PromoManager(models.Manager):
    # custom manager extend models.Manager
    # get_list use for list in views, so we don't need all fields
    # show_expired : bool - show promos which end_date < today
    def get_list(self, show_expired=False):
        fields_list = ["title",
                       "slug",
                       "image",
                       "short_desc",
                       "discount"]
        if show_expired:
            return self.get_queryset().all().only(*fields_list)
        return self.get_queryset().filter(end_date__gte=datetime.today()).only(*fields_list)


class Promo(PolymorphicModel):
    # Promo is Abstract class used PolymorphicModel
    # more information about PolymorphicModel here https://django-polymorphic.readthedocs.io/
    # We need use PolymorphicModel for creating different condition in different types of promo
    # By default we have 3 classes of promo Product_group, Simple_discount, Many_in_stock
    # More information about condition of each subclass inside himself

    title = models.CharField(max_length=255,
                             verbose_name='Title')
    promo_code = models.CharField(max_length=255,
                                  verbose_name='Promotion code',
                                  default=get_random_string(length=6).upper(),
                                  unique=True)
    slug = models.SlugField(unique=True,
                            verbose_name="slug (URL)")
    image = models.ImageField(upload_to='promo/',
                              blank=True,
                              verbose_name="Image")
    description = models.TextField(verbose_name="Description")
    short_desc = models.CharField(verbose_name="Short description for promo",
                                  blank=True,
                                  max_length=255)
    products = models.ManyToManyField('main.Product',
                                      verbose_name='Products',
                                      related_name='related_product')
    discount = models.PositiveIntegerField(default=0,
                                           verbose_name="Discount in %")
    start_date = models.DateTimeField(verbose_name="Start date and time",
                                      default=datetime.now())
    end_date = models.DateTimeField(verbose_name="End date and time",
                                    default=datetime.now() + timedelta(days=30))

    promo_manager = PromoManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title', 'discount']
        index_together = ('id', 'promo_code')

    def get_absolute_url(self):
        return reverse('promo_detail',
                       kwargs={"promo_slug": self.slug})


class ProductGroupDiscount(Promo):
    # Condition: all products from Promoset have to be inside cart

    def condition(self, cart):
        cart_products_ids = set(cart.keys())
        promo_products_ids = set(self.products.values_list('id', flat=True))
        return promo_products_ids.issubset(cart_products_ids)


class SimpleDiscount(Promo):
    # It's just simple discount because we need it.
    # So condition cart is not empty

    def condition(self, cart):
        return True if cart.keys() else False


class CountInStock(Promo):
    # If we have a lot products in stock, we make discount
    # So, condition: check stock count of each product in cart
    need_min_stock_count = models.PositiveIntegerField(verbose_name="Stock of product need",
                                                       default=5)

    def condition(self, cart):
        cart_products_ids = cart.keys()
        cart_products = Product.objects.filter(id__in=cart_products_ids)
        return any(True for product in cart_products if product.stock >= self.need_min_stock_count)
