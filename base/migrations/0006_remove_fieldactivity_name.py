# Generated by Django 4.1.13 on 2024-11-12 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_rename_address_field_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fieldactivity',
            name='name',
        ),
    ]
