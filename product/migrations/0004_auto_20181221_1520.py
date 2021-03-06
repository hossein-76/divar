# Generated by Django 2.1.4 on 2018-12-21 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20181221_1451'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attribute',
            name='valid_values',
        ),
        migrations.RemoveField(
            model_name='category',
            name='products',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='product.Category'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='creation_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
