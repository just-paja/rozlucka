# Generated by Django 2.2 on 2019-04-25 22:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rozlucka', '0009_auto_20190425_2146'),
    ]

    operations = [
        migrations.CreateModel(
            name='StationFacilitator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=63)),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rozlucka.Station')),
            ],
        ),
    ]