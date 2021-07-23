from django.db import models
from mptt.models import MPTTModel, TreeForeignKey  # needs for hierarchical tree of categories
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


# Customer - User extended
# Promo
# Order

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


class Customer(models.Model):
    user = models.ForeignKey(User,
                             verbose_name='Username',
                             on_delete=models.CASCADE)
    phone = models.CharField(max_length=15,
                             verbose_name='Phone number',
                             null=True,
                             blank=True)
    address = models.CharField(max_length=255,
                               verbose_name='Address',
                               null=True,
                               blank=True)
    # orders = models.ManyToManyField('Order',
    #                                 verbose_name='Orders',
    #                                 related_name='related_order')

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)


# class Order(models.Model):
#     STATUS_NEW = 'new'
#     STATUS_IN_PROGRESS = 'in_progress'
#     STATUS_READY = 'is_ready'
#     STATUS_COMPLETED = 'completed'
#
#     BUYING_TYPE_SELF = 'self'
#     BUYING_TYPE_DELIVERY = 'delivery'
#
#     STATUS_CHOICES = (
#         (STATUS_NEW, 'Новый заказ'),
#         (STATUS_IN_PROGRESS, 'Заказ в обработке'),
#         (STATUS_READY, 'Заказ готов'),
#         (STATUS_COMPLETED, 'Заказ выполнен')
#     )
#
#     BUYING_TYPE_CHOICES = (
#         (BUYING_TYPE_SELF, 'Самовывоз'),
#         (BUYING_TYPE_DELIVERY, 'Доставка')
#     )
#
#     customer = models.ForeignKey(Customer,
#                                  verbose_name='Customer',
#                                  related_name='related_orders',
#                                  on_delete=models.CASCADE)
#
#     cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True)
#     status = models.CharField(
#         max_length=100,
#         verbose_name='Статус заказ',
#         choices=STATUS_CHOICES,
#         default=STATUS_NEW
#     )
#     buying_type = models.CharField(
#         max_length=100,
#         verbose_name='Тип заказа',
#         choices=BUYING_TYPE_CHOICES,
#         default=BUYING_TYPE_SELF
#     )
#     comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
#     created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
#
#     def __str__(self):
#         return str(self.id)
