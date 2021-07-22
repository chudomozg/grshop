from django.db import models
from mptt.models import MPTTModel, TreeForeignKey  # needs for hierarchical tree of categories
from django.urls import reverse


# Category - Categories on catalog
# model use mptt, it's realization of Modified Preorder Tree Traversal algorithm, it's more
# faster, then use recursive loop
# more information about algorithm here https://www.sitepoint.com/hierarchical-data-database-2/
# more info about django-mptt https://django-mptt.readthedocs.io/
#
# Product
#
# Cart
# CartProduct
# Customer - User extended
# Promo
# Order?

class Category(MPTTModel):
    name = models.CharField(max_length=255, verbose_name='Category Name', unique=True)
    slug = models.SlugField(unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    # get_absolute_url - convention about naming of method, that return absolute url of instance
    # reverse - make url by urlpatterns
    def get_absolute_url(self):
        return reverse('catalog:product_list_by_category',
                       kwargs={"category_slug": self.slug})


class Product(models.Model):
    title = models.CharField(max_length=255,
                             verbose_name='Title')
    slug = models.SlugField(unique=True,
                            verbose_name="slug (URL)")
    image = models.ImageField(upload_to='products/',
                              blank=True,
                              verbose_name="Image")
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(max_digits=9,
                                decimal_places=2,
                                verbose_name="Price")
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 verbose_name="Category")
    stock = models.PositiveIntegerField(default=1,
                                        verbose_name="Stok")

    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        index_together = ('id', 'slug')

    def get_absolute_url(self):
        return reverse('catalog:product_detail',
                       kwargs={"category_slug": self.category.slug,
                               "product_slug": self.slug})
