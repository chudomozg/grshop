# Generated by Django 3.2.5 on 2021-07-24 04:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20210724_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promo',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 23, 14, 17, 7, 118864), verbose_name='End date and time'),
        ),
        migrations.AlterField(
            model_name='promo',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 24, 14, 17, 7, 118864), verbose_name='Start date and time'),
        ),
    ]