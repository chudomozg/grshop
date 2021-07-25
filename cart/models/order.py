from django.db import models

from grshop.settings import STATUS, DELIVERY_TYPE, BILLING_STATUS, BILLING_TYPE
from main.models import Product
from users.models import UserBase
from users.mixins import DeliveryDetailsMixin
from django.urls import reverse


class Order(DeliveryDetailsMixin):
    # User can make order not for himself
    # that's why we use DeliveryDetailsMixin
    # We will not fix fields from DeliveryDetailsMixin
    # and user can change it in ordering time
    user = models.ForeignKey(UserBase,
                             verbose_name='Customer',
                             related_name='related_orders',
                             on_delete=models.CASCADE)

    status = models.CharField(
        max_length=100,
        verbose_name='Order status',
        choices=STATUS.items(),
        default=STATUS.NEW
    )
    delivery_type = models.CharField(
        max_length=100,
        verbose_name='Delivery type',
        choices=DELIVERY_TYPE.items(),
        default=DELIVERY_TYPE.STANDARD_DELIVERY
    )
    billing_status = models.CharField(
        max_length=100,
        verbose_name='Billing status',
        choices=BILLING_STATUS.items(),
        default=BILLING_STATUS.NOT_PAID
    )
    billing_type = models.CharField(
        max_length=100,
        verbose_name='Billing type',
        choices=BILLING_TYPE.items(),
        default=BILLING_TYPE.IN_OFFICE
    )
    comment = models.TextField(verbose_name='Additional Information',
                               null=True,
                               blank=True)
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Creation date',
                                   help_text='Date of order creation')
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name='Updating date',
                                   help_text='Date of last order update')

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ('-created',)


class OrderItem(models.Model):
    # we will store each product from cart separately
    # because price of products can change
    # So we need fix price for product when create order
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9,
                                decimal_places=2,
                                verbose_name="Price")
    count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)