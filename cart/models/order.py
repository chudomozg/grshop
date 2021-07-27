from django.db import models

from grshop import settings
from main.models import Product
from promo.helpers import get_total_sum_with_promo_discount
from promo.models import Promo
from users.helpers import get_delivery_detail_fields_dict
from users.models import UserBase
from users.mixins import DeliveryDetailsMixin
from django.urls import reverse


def get_order_hash(cart, promo):
    # Use only after adding OrderItems
    out_str = ""
    for item in cart:
        out_str += "product={}&price={}&count={}".format(item['product'], item['price'], item['count'])
    out_str += str(promo)
    return hash(out_str)


def check_billing():
    # stub function
    # in this demo, we don't use any payment system
    # so use this function for payment system
    return settings.BILLING_STATUS['NOT_PAID']


def create_order(user_id, cart, promo, order_hash, checkout_form_data):
    # create instance of order with args
    # get_delivery_detail_fields_dict() helps to avoid code duplication
    other_kwargs = get_delivery_detail_fields_dict(checkout_form_data)
    promo_id = None
    if promo:
        total_sum = get_total_sum_with_promo_discount(cart, promo)
        promo_id = promo.pk
    else:
        total_sum = cart.get_total_price()
    order = Order.objects.create(user_id=user_id,
                                 delivery_type=checkout_form_data['delivery_type'],
                                 billing_type=checkout_form_data['billing_type'],
                                 billing_status=check_billing(),
                                 comment=checkout_form_data['comment'],
                                 order_hash=order_hash,
                                 total_sum=total_sum,
                                 **other_kwargs
                                 )
    order.save()
    if promo_id:
        order.promo.add(promo_id)
        order.save()
    order_id = order.pk
    for item in cart:
        OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'], count=item['count'])


class Order(DeliveryDetailsMixin):
    # User can make order not for himself
    # that's why we use DeliveryDetailsMixin
    # We will not fix fields from DeliveryDetailsMixin
    # and user can change it in ordering time
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name='Customer',
                             related_name='related_orders',
                             on_delete=models.CASCADE)

    status = models.CharField(
        max_length=100,
        verbose_name='Order status',
        choices=settings.STATUS.items(),
        default=settings.STATUS['NEW']
    )
    delivery_type = models.CharField(
        max_length=100,
        verbose_name='Delivery type',
        choices=settings.DELIVERY_TYPE.items(),
        default=settings.DELIVERY_TYPE['STANDARD_DELIVERY']
    )
    billing_status = models.CharField(
        max_length=100,
        verbose_name='Billing status',
        choices=settings.BILLING_STATUS.items(),
        default=settings.BILLING_STATUS['NOT_PAID']
    )
    billing_type = models.CharField(
        max_length=100,
        verbose_name='Billing type',
        choices=settings.BILLING_TYPE.items(),
        default=settings.BILLING_TYPE['IN_OFFICE']
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
    # order_hash it's hash of cart for prevent duplicate order
    order_hash = models.CharField(max_length=100,
                                  null=True,
                                  blank=True)
    promo = models.ManyToManyField(Promo, related_name="promos")
    total_sum = models.PositiveIntegerField(verbose_name='Total order sum',
                                            null=True,
                                            blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ('-created',)


class OrderItem(models.Model):
    # we will store each product from cart separately
    # because price of products can change
    # So we need fix price for product when create order
    order = models.ForeignKey(Order,
                              related_name='order',
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
