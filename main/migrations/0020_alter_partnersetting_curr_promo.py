# Generated by Django 3.2.3 on 2021-08-25 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20210817_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partnersetting',
            name='curr_promo',
            field=models.ManyToManyField(blank=True, null=True, to='main.Promo'),
        ),
    ]