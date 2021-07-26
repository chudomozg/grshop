# Generated by Django 3.2.5 on 2021-07-26 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('promo', '0007_auto_20210726_1951'),
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='promo',
            field=models.ManyToManyField(related_name='promos', to='promo.Promo'),
        ),
        migrations.AddField(
            model_name='order',
            name='total_sum',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Total order sum'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='cart.order'),
        ),
    ]
