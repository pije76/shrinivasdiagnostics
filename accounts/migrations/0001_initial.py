# Generated by Django 4.1.1 on 2022-10-23 10:33

import accounts.managers
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('state', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('pin_code', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Address',
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(error_messages={'unique': 'This email has already been registered.'}, max_length=255, unique=True, verbose_name='Email Address')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('birth_date', models.DateField(null=True)),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], default=None, max_length=255, null=True)),
                ('relation', models.CharField(blank=True, choices=[('father', 'Male'), ('mother', 'Female'), ('spouse', 'Spouse'), ('son', 'Son'), ('daughter', 'Daughter'), ('family', 'Family')], default=None, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Patient',
                'verbose_name_plural': 'Patient',
            },
        ),
        migrations.CreateModel(
            name='UOTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('issuer', models.CharField(help_text='One of Email or Msisdn', max_length=255)),
                ('purpose', models.CharField(choices=[('signin', 'Sign In')], default='signin', max_length=15)),
                ('otp', models.CharField(db_index=True, max_length=10)),
                ('secret', models.CharField(db_index=True, max_length=255)),
                ('valid_until', models.DateTimeField(blank=True, editable=False, null=True)),
                ('valid_until_timestamp', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(error_messages={'unique': 'This email has already been registered.'}, max_length=255, unique=True, verbose_name='Email Address')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('birth_date', models.DateField(null=True)),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], default=None, max_length=255, null=True)),
                ('is_active', models.BooleanField(blank=True, default=False, null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profile',
            },
            managers=[
                ('objects', accounts.managers.UserManager()),
            ],
        ),
    ]
