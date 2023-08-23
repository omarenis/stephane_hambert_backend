# Generated by Django 4.2.2 on 2023-08-20 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_management', '0002_rename_description_collection_content'),
    ]

    operations = [
        migrations.RenameField(
            model_name='promo',
            old_name='label',
            new_name='title',
        ),
        migrations.AlterField(
            model_name='product',
            name='category_set',
            field=models.ManyToManyField(blank=True, to='stock_management.category'),
        ),
    ]
