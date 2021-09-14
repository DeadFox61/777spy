# Generated by Django 3.2.3 on 2021-09-13 17:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_auto_20210912_1856'),
    ]

    operations = [
        migrations.AddField(
            model_name='partnersetting',
            name='percent',
            field=models.IntegerField(default=25, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='usersetting',
            name='checked_nums',
            field=models.JSONField(blank=True, default=[]),
        ),
        migrations.AlterField(
            model_name='usersetting',
            name='individual_stats',
            field=models.JSONField(blank=True, default={}),
        ),
    ]
