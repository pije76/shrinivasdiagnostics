# Generated by Django 4.1.3 on 2022-12-05 23:18

import autoslug.fields
import cities_light.abstract_models
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
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('name_ascii', models.CharField(blank=True, db_index=True, max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name_ascii')),
                ('geoname_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('alternate_names', models.TextField(blank=True, default='', null=True)),
                ('code2', models.CharField(blank=True, max_length=2, null=True, unique=True)),
                ('code3', models.CharField(blank=True, max_length=3, null=True, unique=True)),
                ('continent', models.CharField(choices=[('OC', 'Oceania'), ('EU', 'Europe'), ('AF', 'Africa'), ('NA', 'North America'), ('AN', 'Antarctica'), ('SA', 'South America'), ('AS', 'Asia')], db_index=True, max_length=2)),
                ('tld', models.CharField(blank=True, db_index=True, max_length=5)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'verbose_name_plural': 'countries',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('name_ascii', models.CharField(blank=True, db_index=True, max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name_ascii')),
                ('geoname_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('alternate_names', models.TextField(blank=True, default='', null=True)),
                ('display_name', models.CharField(max_length=200)),
                ('geoname_code', models.CharField(blank=True, db_index=True, max_length=50, null=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='address.country')),
            ],
            options={
                'verbose_name': 'region/state',
                'verbose_name_plural': 'regions/states',
                'ordering': ['name'],
                'abstract': False,
                'unique_together': {('country', 'name'), ('country', 'slug')},
            },
        ),
        migrations.CreateModel(
            name='SubRegion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('name_ascii', models.CharField(blank=True, db_index=True, max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name_ascii')),
                ('geoname_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('alternate_names', models.TextField(blank=True, default='', null=True)),
                ('display_name', models.CharField(max_length=200)),
                ('geoname_code', models.CharField(blank=True, db_index=True, max_length=50, null=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='address.country')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.region')),
            ],
            options={
                'verbose_name': 'SubRegion',
                'verbose_name_plural': 'SubRegions',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('name_ascii', models.CharField(blank=True, db_index=True, max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name_ascii')),
                ('geoname_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('alternate_names', models.TextField(blank=True, default='', null=True)),
                ('display_name', models.CharField(max_length=200)),
                ('search_names', cities_light.abstract_models.ToSearchTextField(blank=True, db_index=True, default='', max_length=4000)),
                ('latitude', models.DecimalField(blank=True, decimal_places=5, max_digits=8, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=5, max_digits=8, null=True)),
                ('population', models.BigIntegerField(blank=True, db_index=True, null=True)),
                ('feature_code', models.CharField(blank=True, db_index=True, max_length=10, null=True)),
                ('timezone', models.CharField(max_length=40)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='address.country')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.region')),
                ('subregion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.subregion')),
            ],
            options={
                'verbose_name_plural': 'cities',
                'ordering': ['name'],
                'abstract': False,
                'unique_together': {('region', 'subregion', 'name'), ('region', 'subregion', 'slug')},
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('pin_code', models.CharField(blank=True, max_length=255, null=True)),
                ('zip', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.city')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.country')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.region')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_address', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Address',
            },
        ),
    ]
