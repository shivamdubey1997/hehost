# Generated by Django 4.0.3 on 2022-09-12 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_cart_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.PositiveBigIntegerField(default=2),
        ),
    ]
