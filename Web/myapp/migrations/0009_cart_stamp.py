# Generated by Django 3.0 on 2021-02-07 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='stamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
