# Generated by Django 2.2 on 2019-04-04 07:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Puzzle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('question', models.TextField(max_length=255)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rozlucka.Answer')),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visited', models.BooleanField(default=False)),
                ('skipped', models.BooleanField(default=False)),
                ('next', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='prev', to='rozlucka.Station')),
                ('puzzle', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rozlucka.Puzzle')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('due', models.DateTimeField()),
                ('started', models.BooleanField(default=False)),
                ('initial_station', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rozlucka.Station')),
            ],
        ),
    ]
