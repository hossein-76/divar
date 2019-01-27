# Generated by Django 2.1.4 on 2019-01-27 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_report'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='detail',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='reason',
            field=models.CharField(choices=[('inappropriate content', 'inappropriate content'), ('spam content', 'spam content')], default='inappropriate content', max_length=255),
        ),
        migrations.AlterField(
            model_name='report',
            name='status',
            field=models.CharField(choices=[('approved', 'approved'), ('rejected', 'rejected'), ('pending', 'pending')], default='pending', max_length=255),
        ),
    ]