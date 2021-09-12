# Generated by Django 3.2 on 2021-04-22 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_auto_20210411_1221'),
    ]

    operations = [
        migrations.CreateModel(
            name='Baccarat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('bacc_id', models.CharField(max_length=30)),
                ('provider', models.CharField(default='Evolution', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='BaccGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_state', models.CharField(max_length=50)),
                ('baccarat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.baccarat')),
            ],
        ),
    ]