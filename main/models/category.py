from django.db import models
from mptt.models import MPTTModel, TreeForeignKey  # needs for hierarchical tree of categories
from django.urls import reverse

class Category(MPTTModel):
    # Category - Categories on catalog
    # model use mptt, it's realization of Modified Preorder Tree Traversal algorithm, it's more
    # faster, then use recursive loop
    # more information about algorithm here https://www.sitepoint.com/hierarchical-data-database-2/
    # more info about django-mptt https://django-mptt.readthedocs.io/
    name = models.CharField(max_length=255, verbose_name='Category Name', unique=True)
    slug = models.SlugField(unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # get_absolute_url - convention about naming of method, that return absolute url of instance
        # reverse - make url by urlpatterns
        return reverse('catalog:product_list_by_category',
                       kwargs={"category_slug": self.slug})