# Generated by Django 5.1.3 on 2024-11-23 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='prce',
            new_name='price',
        ),
    ]
