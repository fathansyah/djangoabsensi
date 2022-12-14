# Generated by Django 4.1.1 on 2022-10-20 08:57

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Absen_rider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('Absensi_status', models.TextField(default='Sudah Absen')),
                ('Arearider', models.CharField(choices=[('A2', 'Semarang Utara'), ('A1', 'Semarang Barat'), ('A3', 'Ngaliyan'), ('B1', 'Tugu'), ('B2', 'Mijen')], max_length=30)),
                ('J_paket', models.CharField(max_length=255)),
                ('F_paket', models.CharField(max_length=255)),
                ('Cod', models.CharField(max_length=255)),
                ('Tanggal_absen', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Absencaptain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('Absensi_status', models.TextField(default='Sudah Absen')),
                ('Tanggal_absen', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Absenfl_staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('Absensi_status', models.TextField(default='Sudah Absen')),
                ('Tanggal_absen', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Absenstaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('Absensi_status', models.TextField(default='Sudah Absen')),
                ('Tanggal_absen', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Is Admin')),
                ('is_fl', models.BooleanField(default=False, verbose_name='Is Freelance')),
                ('is_captain', models.BooleanField(default=False, verbose_name='Is Captain')),
                ('is_staff', models.BooleanField(default=False, verbose_name='is Staff')),
                ('is_rider', models.BooleanField(default=False, verbose_name='is Rider')),
                ('branch', models.CharField(max_length=100)),
                ('nik', models.CharField(max_length=100)),
                ('telp', models.CharField(max_length=14)),
                ('kodehub', models.CharField(max_length=100)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
