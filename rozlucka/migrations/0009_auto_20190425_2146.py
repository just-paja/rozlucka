# Generated by Django 2.2 on 2019-04-25 21:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rozlucka', '0008_answerattempt_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='puzzle',
            name='answer',
        ),
        migrations.AddField(
            model_name='answer',
            name='puzzle',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='rozlucka.Puzzle'),
        ),
    ]
