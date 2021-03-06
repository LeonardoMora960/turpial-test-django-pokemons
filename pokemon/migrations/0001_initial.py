# Generated by Django 3.0.8 on 2020-07-21 07:08

from django.conf import settings
import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Areas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=100)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Regions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=100)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abilities', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=300), size=None)),
                ('capture_rate', models.CharField(blank=True, default='', max_length=300, null=True)),
                ('color', models.CharField(blank=True, default='', max_length=300, null=True)),
                ('flavor_text', models.CharField(blank=True, default='', max_length=300, null=True)),
                ('height', models.CharField(blank=True, default='', max_length=300, null=True)),
                ('moves', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=1500), size=500)),
                ('name', models.CharField(blank=True, default='', max_length=300, null=True)),
                ('sprites', django.contrib.postgres.fields.jsonb.JSONField()),
                ('stats', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.jsonb.JSONField(), size=None)),
                ('types', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=300), size=None)),
                ('weight', models.CharField(blank=True, default='', max_length=300, null=True)),
                ('areas', models.ManyToManyField(related_name='species', to='pokemon.Areas')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Storage_Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nick_name', models.CharField(blank=True, default='', max_length=100)),
                ('is_party_member', models.BooleanField(blank=True)),
                ('specie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pokemon.Species')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('specie',),
            },
        ),
        migrations.CreateModel(
            name='Locations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=100)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='pokemon.Regions')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='areas',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='areas', to='pokemon.Locations'),
        ),
    ]
