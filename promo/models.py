from datetime import datetime, timedelta
from django.db import models
from django.urls import reverse
from main.models import Product


def get_promos_list(show_expired=False):
    # Helper
    # Use for list in views, so we don't need all fields
    # show_expired : bool - show promos which end_date < today
    fields_list = ["title",
                   "slug",
                   "image",
                   "short_desc",
                   "discount"]
    if show_expired:
        return Promo.objects.all().only(*fields_list)
    return Promo.objects.filter(end_date__gte=datetime.today()).only(*fields_list)


class Promo(models.Model):
    title = models.CharField(max_length=255,
                             verbose_name='Title')
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

    def __str__(self):
        return "{}: discount {}%".format(self.title, self.discount)

    class Meta:
        ordering = ['title', 'discount']
        index_together = ('id', 'slug')

    def get_absolute_url(self):
        return reverse('promo_detail',
                       kwargs={"promo_slug": self.slug})
