# Generated by Django 3.1.7 on 2021-04-11 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20210410_2355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='tlg_id',
            field=models.CharField(blank=True, default='', max_length=20),
            preserve_default=False,
        ),
    ]