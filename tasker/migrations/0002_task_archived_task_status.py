# Generated by Django 5.1.1 on 2024-12-14 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='archived',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
