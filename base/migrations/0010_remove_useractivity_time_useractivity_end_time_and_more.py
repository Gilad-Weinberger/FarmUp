# Generated by Django 4.1.13 on 2024-11-14 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_alter_lineactivity_start_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useractivity',
            name='time',
        ),
        migrations.AddField(
            model_name='useractivity',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='useractivity',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]