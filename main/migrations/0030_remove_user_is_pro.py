# Generated by Django 3.2.3 on 2021-09-01 07:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0029_auto_20210901_0711'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_pro',
        ),
    ]
