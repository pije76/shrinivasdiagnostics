# Generated by Django 4.1.2 on 2022-10-25 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, null=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('tags', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('available', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('prerequisites', models.CharField(blank=True, max_length=255, null=True)),
                ('samplecutoff', models.CharField(blank=True, max_length=255, null=True)),
                ('report', models.TextField(blank=True)),
                ('note', models.TextField(blank=True)),
                ('component', models.CharField(blank=True, max_length=255, null=True)),
                ('speciment', models.CharField(blank=True, max_length=255, null=True)),
                ('method', models.CharField(blank=True, max_length=255, null=True)),
                ('cutofftime', models.CharField(blank=True, max_length=255, null=True)),
                ('quantitytemperature', models.CharField(blank=True, max_length=255, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_product', to='shop.category')),
            ],
            options={
                'ordering': ('name',),
                'index_together': {('id', 'slug')},
            },
        ),
    ]
