# Generated by Django 3.1.3 on 2021-05-12 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_item_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
    ]
