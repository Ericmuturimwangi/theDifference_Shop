# Generated by Django 5.0.7 on 2024-07-22 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_category_options_product_is_sale_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='is_sale',
            field=models.BooleanField(default=True),
        ),
    ]