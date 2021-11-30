# Generated by Django 3.2.7 on 2021-09-10 06:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdDate', models.DateTimeField()),
                ('title', models.CharField(max_length=255)),
                ('abstract', models.TextField()),
                ('content', models.TextField()),
                ('publishedDate', models.DateTimeField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Strand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdDate', models.DateTimeField()),
                ('short', models.CharField(max_length=10, unique=True)),
                ('strand', models.CharField(max_length=50)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdDate', models.DateTimeField()),
                ('short', models.CharField(max_length=10, unique=True)),
                ('source', models.CharField(max_length=50)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MapLayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdDate', models.DateTimeField()),
                ('name', models.CharField(max_length=50)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MapEntryType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdDate', models.DateTimeField()),
                ('short', models.CharField(max_length=10)),
                ('type', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MapEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdDate', models.DateTimeField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('layer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='core.maplayer')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.mapentrytype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MapDrawing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdDate', models.DateTimeField()),
                ('name', models.CharField(max_length=50)),
                ('layer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='drawings', to='core.maplayer')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Interpretation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdDate', models.DateTimeField()),
                ('interpretation', models.TextField()),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.entry')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EntryType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdDate', models.DateTimeField()),
                ('short', models.CharField(max_length=4, unique=True)),
                ('type', models.CharField(max_length=50)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='entry',
            name='map_entry',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entries', to='core.mapentry'),
        ),
        migrations.AddField(
            model_name='entry',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='entry',
            name='source',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.source'),
        ),
        migrations.AddField(
            model_name='entry',
            name='strand',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.strand'),
        ),
        migrations.AddField(
            model_name='entry',
            name='type',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.entrytype'),
        ),
    ]