# Generated by Django 3.2.7 on 2021-09-10 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210910_0855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mapentrytype',
            name='icon',
            field=models.ImageField(upload_to=''),
        ),
    ]