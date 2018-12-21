# Generated by Django 2.1.4 on 2018-12-21 18:46

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_auto_20181221_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appmanager',
            name='categories',
            field=models.ManyToManyField(blank=True, to='product.Category'),
        ),
        migrations.AlterField(
            model_name='appmanager',
            name='cities',
            field=models.ManyToManyField(blank=True, to='product.City'),
        ),
        migrations.AlterField(
            model_name='cpmapper',
            name='products',
            field=models.ManyToManyField(blank=True, to='product.Product'),
        ),
        migrations.AlterField(
            model_name='cvmapper',
            name='vicinities',
            field=models.ManyToManyField(blank=True, to='product.Vicinity'),
        ),
        migrations.AlterField(
            model_name='product',
            name='attributes',
            field=django_mysql.models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ManyToManyField(blank=True, to='product.ProductImage'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='alt',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='vpmapper',
            name='products',
            field=models.ManyToManyField(blank=True, to='product.Product'),
        ),
    ]
