# Generated by Django 4.0.7 on 2022-08-26 01:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_record_region_records'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='region',
            name='records',
        ),
    ]
