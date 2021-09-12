# Generated by Django 3.2.3 on 2021-09-12 18:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_auto_20210614_0910'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255, unique=True)),
                ('free_days', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='number',
            name='is_new',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_pro',
        ),
        migrations.AddField(
            model_name='user',
            name='is_partner',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='referrer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usersetting',
            name='checked_nums',
            field=models.JSONField(default=[]),
        ),
        migrations.AddField(
            model_name='usersetting',
            name='individual_stats',
            field=models.JSONField(default={}),
        ),
        migrations.AlterField(
            model_name='usersetting',
            name='curr_roulettes',
            field=models.ManyToManyField(blank=True, null=True, to='main.Roulette'),
        ),
        migrations.CreateModel(
            name='RefLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255, unique=True)),
                ('source', models.CharField(blank=True, max_length=255)),
                ('comment', models.CharField(blank=True, max_length=255)),
                ('promo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.promo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PartnerSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance_current', models.IntegerField(default=0)),
                ('balance_wait', models.IntegerField(default=0)),
                ('balance_paid', models.IntegerField(default=0)),
                ('curr_promo', models.ManyToManyField(blank=True, null=True, to='main.Promo')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ClickEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=25, unique=True)),
                ('link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.reflink')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='referrer_link',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='referrals', to='main.reflink'),
        ),
    ]