# Generated by Django 3.1.7 on 2021-04-11 01:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20210411_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='tlg_bot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.tlgbot'),
        ),
    ]