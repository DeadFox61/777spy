# Generated by Django 3.2.3 on 2021-09-01 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_auto_20210901_0651'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partnersetting',
            name='clicks_count',
        ),
        migrations.RemoveField(
            model_name='partnersetting',
            name='reg_count',
        ),
    ]
