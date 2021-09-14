# Generated by Django 3.2 on 2021-05-29 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_roulette_new_stats'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParseData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.IntegerField()),
                ('evo_id', models.CharField(max_length=120)),
            ],
        ),
        migrations.RemoveField(
            model_name='rouletteinfo',
            name='roulette',
        ),
        migrations.DeleteModel(
            name='Setting',
        ),
        migrations.DeleteModel(
            name='RouletteInfo',
        ),
    ]
