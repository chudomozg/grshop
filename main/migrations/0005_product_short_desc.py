# Generated by Django 3.2.5 on 2021-07-23 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_product_on_front'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='short_desc',
            field=models.CharField(blank=True, max_length=255, verbose_name='Short description for promo'),
        ),
    ]
