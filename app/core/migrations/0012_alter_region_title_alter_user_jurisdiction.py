# Generated by Django 4.0.7 on 2022-08-25 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_rename_region_user_jurisdiction_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='region',
            name='title',
            field=models.CharField(choices=[('NT', 'Northern Territory'), ('QLD', 'Queensland'), ('TAS', 'Tasmania'), ('NSW', 'New South Wales'), ('SA', 'South Australia'), ('VIC', 'Victoria'), ('WA', 'Western Australia'), ('SB', 'Solomon Islands'), ('COMM', 'Commonwealth'), ('OTHER', 'Other'), ('ALL', 'All'), ('NFK', 'Norfolk Island')], default='OTHER', max_length=5),
        ),
        migrations.AlterField(
            model_name='user',
            name='jurisdiction',
            field=models.CharField(choices=[('NT', 'Northern Territory'), ('QLD', 'Queensland'), ('TAS', 'Tasmania'), ('NSW', 'New South Wales'), ('SA', 'South Australia'), ('VIC', 'Victoria'), ('WA', 'Western Australia'), ('SB', 'Solomon Islands'), ('COMM', 'Commonwealth'), ('OTHER', 'Other'), ('ALL', 'All'), ('NFK', 'Norfolk Island')], default='OTHER', max_length=5),
        ),
    ]
