# Generated by Django 2.2 on 2019-04-23 15:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rozlucka', '0007_auto_20190423_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='answerattempt',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]