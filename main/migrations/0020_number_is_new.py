# Generated by Django 3.2 on 2021-04-30 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_user_online_time_sec'),
    ]

    operations = [
        migrations.AddField(
            model_name='number',
            name='is_new',
            field=models.BooleanField(default=True),
        ),
    ]
