# Generated by Django 3.1.7 on 2021-03-31 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_remove_tlgmsg_msg_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='tlgmsg',
            name='msg_id',
            field=models.IntegerField(default=-1),
        ),
    ]
