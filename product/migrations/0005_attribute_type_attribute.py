# Generated by Django 2.1.4 on 2018-12-21 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20181221_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='attribute',
            name='type_attribute',
            field=models.CharField(choices=[('numeric', 'numeric'), ('value', 'value')], default='value', max_length=100),
        ),
    ]