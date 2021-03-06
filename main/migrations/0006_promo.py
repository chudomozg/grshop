# Generated by Django 3.2.5 on 2021-07-24 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_product_short_desc'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(unique=True, verbose_name='slug (URL)')),
                ('image', models.ImageField(blank=True, upload_to='promo/', verbose_name='Image')),
                ('description', models.TextField(verbose_name='Description')),
                ('short_desc', models.CharField(blank=True, max_length=255, verbose_name='Short description for promo')),
                ('discount', models.PositiveIntegerField(default=0, verbose_name='Discount in %')),
                ('products', models.ManyToManyField(related_name='related_product', to='main.Product', verbose_name='Products')),
            ],
            options={
                'ordering': ['title', 'discount'],
                'index_together': {('id', 'slug')},
            },
        ),
    ]
