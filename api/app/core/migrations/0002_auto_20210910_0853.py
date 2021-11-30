# Generated by Django 3.2.7 on 2021-09-10 06:53

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mapdrawing',
            name='geometry',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='mapdrawing',
            name='properties',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='mapentrytype',
            name='icon',
            field=models.CharField(default='default', max_length=50),
        ),
    ]