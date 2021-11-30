# Generated by Django 3.2.7 on 2021-09-10 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20210910_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='maplayer',
            name='strand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='layers', to='core.strand'),
        ),
        migrations.AddField(
            model_name='source',
            name='mission',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sources', to='core.mission'),
        ),
        migrations.AlterField(
            model_name='mission',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]