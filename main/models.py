from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Customer - User extended
# Promo
# Order



#
# class Customer(models.Model):
#     user = models.ForeignKey(User,
#                              verbose_name='Username',
#                              on_delete=models.CASCADE)
#     phone = models.CharField(max_length=15,
#                              verbose_name='Phone number',
#                              null=True,
#                              blank=True)
#     address = models.CharField(max_length=255,
#                                verbose_name='Address',
#                                null=True,
#                                blank=True)
#     # orders = models.ManyToManyField('Order',
#     #                                 verbose_name='Orders',
#     #                                 related_name='related_order')
#
#     def __str__(self):
#         return "{} {}".format(self.user.first_name, self.user.last_name)

