# Generated by Django 3.1.3 on 2021-05-10 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20210510_1808'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='type',
        ),
    ]
