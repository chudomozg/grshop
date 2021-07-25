from django.db import models


class DeliveryDetailsMixin(models.Model):
    # Delivery details
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    country = models.CharField(max_length=20, blank=True)
    area = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=150, blank=True)
    address = models.CharField(max_length=255, blank=True)
    postcode = models.CharField(max_length=12, blank=True)

    class Meta:
        abstract = True
