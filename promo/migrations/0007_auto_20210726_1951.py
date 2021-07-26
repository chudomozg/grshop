# Generated by Django 3.2.5 on 2021-07-26 09:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promo', '0006_auto_20210726_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promo',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 25, 19, 51, 49, 966266), verbose_name='End date and time'),
        ),
        migrations.AlterField(
            model_name='promo',
            name='promo_code',
            field=models.CharField(default='JOTJBK', max_length=255, unique=True, verbose_name='Promotion code'),
        ),
        migrations.AlterField(
            model_name='promo',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 26, 19, 51, 49, 966266), verbose_name='Start date and time'),
        ),
        migrations.AlterIndexTogether(
            name='promo',
            index_together={('id', 'promo_code')},
        ),
    ]
