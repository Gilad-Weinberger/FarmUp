# Generated by Django 4.1.13 on 2024-11-14 10:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alter_fieldactivity_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lineactivity',
            name='start_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
