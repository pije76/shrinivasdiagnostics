# Generated by Django 2.0.5 on 2018-10-24 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='Order',
            new_name='order',
        ),
    ]
