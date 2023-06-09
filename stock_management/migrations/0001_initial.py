# Generated by Django 4.1.7 on 2023-07-02 21:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('number_products', models.BigIntegerField(default=0)),
                ('number_purchases', models.BigIntegerField(default=0)),
                ('total_gain', models.FloatField(default=0.0)),
            ],
            options={
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='mages/collections')),
                ('label', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('number_products', models.BigIntegerField(default=0)),
                ('number_purchases', models.BigIntegerField(default=0)),
                ('total_gain', models.FloatField(default=0.0)),
            ],
            options={
                'db_table': 'collections',
            },
        ),
        migrations.CreateModel(
            name='Promo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, unique=True)),
                ('datetime_start', models.DateTimeField()),
                ('datetime_end', models.DateTimeField()),
                ('percentage', models.FloatField()),
                ('number_products', models.BigIntegerField(default=0)),
                ('number_purchases', models.BigIntegerField(default=0)),
                ('total_gain', models.FloatField(default=0.0)),
            ],
            options={
                'db_table': 'promos',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('code', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('price', models.FloatField()),
                ('current_quantity', models.BigIntegerField(default=1)),
                ('tva', models.FloatField()),
                ('image', models.ImageField(upload_to='images/products')),
                ('number_purchases', models.BigIntegerField(default=0)),
                ('ingredients', models.TextField()),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField()),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='stock_management.category')),
                ('collection', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='stock_management.collection')),
                ('promo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='stock_management.promo')),
            ],
            options={
                'db_table': 'products',
            },
        ),
    ]
