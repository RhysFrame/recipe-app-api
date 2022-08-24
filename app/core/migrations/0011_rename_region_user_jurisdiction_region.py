# Generated by Django 4.0.7 on 2022-08-24 02:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_user_region'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='region',
            new_name='jurisdiction',
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('NT', 'Northern Territory'), ('QLD', 'Queensland'), ('TAS', 'Tasmania'), ('NSW', 'New South Wales'), ('SA', 'South Australia'), ('VIC', 'Victoria'), ('WA', 'Western Australia'), ('SB', 'Solomon Islands'), ('COMM', 'Commonwealth'), ('OTHER', 'Other'), ('ALL', 'All')], default='OTHER', max_length=5)),
                ('data_type', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
