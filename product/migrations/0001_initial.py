# Generated by Django 2.1.4 on 2018-12-21 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='AttributeChoiceValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='childs', to='product.Category')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CPMapper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.City')),
            ],
        ),
        migrations.CreateModel(
            name='CVMapper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.City')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True)),
                ('price', models.FloatField()),
                ('creation_time', models.DateTimeField(blank=True, default=None, null=True)),
                ('attributes', models.ManyToManyField(to='product.Attribute')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product')),
                ('alt', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Vicinity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.City')),
            ],
        ),
        migrations.CreateModel(
            name='VPMapper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.City')),
                ('vicinities', models.ManyToManyField(to='product.Vicinity')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ManyToManyField(to='product.ProductImage'),
        ),
        migrations.AddField(
            model_name='product',
            name='vicinity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Vicinity'),
        ),
        migrations.AddField(
            model_name='cvmapper',
            name='vicinities',
            field=models.ManyToManyField(to='product.Vicinity'),
        ),
        migrations.AddField(
            model_name='cpmapper',
            name='vicinities',
            field=models.ManyToManyField(to='product.Vicinity'),
        ),
        migrations.AddField(
            model_name='category',
            name='products',
            field=models.ManyToManyField(to='product.Product'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='valid_values',
            field=models.ManyToManyField(to='product.AttributeChoiceValue'),
        ),
    ]
