# Generated by Django 3.2.3 on 2021-08-17 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_auto_20210812_2015'),
    ]

    operations = [
        migrations.RenameField(
            model_name='partnersetting',
            old_name='balance',
            new_name='balance_current',
        ),
        migrations.RenameField(
            model_name='partnersetting',
            old_name='all_time_pays',
            new_name='balance_paid',
        ),
        migrations.AddField(
            model_name='partnersetting',
            name='balance_wait',
            field=models.IntegerField(default=0),
        ),
    ]
