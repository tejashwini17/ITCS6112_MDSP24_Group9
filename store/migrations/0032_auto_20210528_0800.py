# Generated by Django 3.1.3 on 2021-05-28 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0031_auto_20210526_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Delivered', 'Delivered')], default='Pending', max_length=200, null=True),
        ),
    ]