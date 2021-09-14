# Generated by Django 3.2 on 2021-06-14 09:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_auto_20210529_1332'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaccRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('rule_type', models.IntegerField()),
                ('count', models.IntegerField()),
                ('color', models.IntegerField()),
                ('is_tg_on', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TlgMsgBacc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_sended', models.BooleanField(default=False)),
                ('bacc_name', models.CharField(max_length=40)),
                ('rule_name', models.CharField(max_length=20)),
                ('count', models.IntegerField()),
                ('is_stoped', models.BooleanField(default=False)),
                ('msg_id', models.IntegerField(default=-1)),
                ('rule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.baccrule')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='baccarat',
            name='game_state',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='baccarat',
            name='sort_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usersetting',
            name='curr_baccarats',
            field=models.ManyToManyField(blank=True, null=True, to='main.Baccarat'),
        ),
        migrations.DeleteModel(
            name='BaccGame',
        ),
    ]
