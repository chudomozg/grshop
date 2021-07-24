from django.db import models
from django.urls import reverse
from ..models import Category


class Product(models.Model):
    title = models.CharField(max_length=255,
                             verbose_name='Title')
    slug = models.SlugField(unique=True,
                            verbose_name="slug (URL)")
    image = models.ImageField(upload_to='products/',
                              blank=True,
                              verbose_name="Image")
    description = models.TextField(verbose_name="Description")
    short_desc = models.CharField(verbose_name="Short description for promo",
                                  blank=True,
                                  max_length=255)
    price = models.DecimalField(max_digits=9,
                                decimal_places=2,
                                verbose_name="Price")
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 verbose_name="Category")
    stock = models.PositiveIntegerField(default=1,
                                        verbose_name="Stok")

    available = models.BooleanField(default=True)
    on_front = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        index_together = ('id', 'slug')

    def get_absolute_url(self):
        return reverse('catalog:product_detail',
                       kwargs={"category_slug": self.category.slug,
                               "product_slug": self.slug})
