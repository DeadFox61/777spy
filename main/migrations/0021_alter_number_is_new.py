# Generated by Django 3.2 on 2021-04-30 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_number_is_new'),
    ]

    operations = [
        migrations.AlterField(
            model_name='number',
            name='is_new',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
