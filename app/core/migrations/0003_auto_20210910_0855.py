# Generated by Django 3.2.7 on 2021-09-10 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210910_0853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mapdrawing',
            name='geometry',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='mapdrawing',
            name='properties',
            field=models.JSONField(default=dict),
        ),
    ]
