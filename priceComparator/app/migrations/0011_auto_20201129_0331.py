# Generated by Django 3.1 on 2020-11-29 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_productprice_typeprice'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productprice',
            old_name='product_id',
            new_name='producto',
        ),
        migrations.AlterField(
            model_name='product',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='updated_date',
            field=models.DateTimeField(auto_now=True, default=None),
            preserve_default=False,
        ),
    ]
