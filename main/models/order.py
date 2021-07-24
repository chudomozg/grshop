from django.db import models
from django.urls import reverse

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