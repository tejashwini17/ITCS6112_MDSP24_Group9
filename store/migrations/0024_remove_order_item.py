# Generated by Django 3.1.3 on 2021-05-25 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0023_order_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='item',
        ),
    ]
