# Generated by Django 2.2 on 2019-04-23 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rozlucka', '0003_station_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='station',
            name='name',
            field=models.CharField(default=None, max_length=63),
            preserve_default=False,
        ),
    ]
