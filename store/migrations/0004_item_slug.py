# Generated by Django 2.2.7 on 2019-12-10 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20191210_1538'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(default='product-1'),
            preserve_default=False,
        ),
    ]
