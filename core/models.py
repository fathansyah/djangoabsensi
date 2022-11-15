from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_admin = models.BooleanField("Is Admin", default=False)
    is_fl = models.BooleanField("Is Freelance", default=False)
    is_captain = models.BooleanField("Is Captain", default=False)
    is_staff = models.BooleanField("is Staff", default=False)
    is_rider = models.BooleanField("is Rider", default=False)
    
    branch = models.CharField(max_length=100)
   
    nik = models.CharField(max_length=100)

    telp = models.CharField(max_length=14)

    kodehub = models.CharField(max_length=100)

class Absenfl_staff(models.Model):
    username = models.CharField(max_length=255)
    Absensi_status = models.TextField(default ="Sudah Absen")
    Tanggal_absen = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username

class Absencaptain(models.Model):
    username = models.CharField(max_length=255)
    J_hold = models.CharField(max_length=255)
    Absensi_status = models.TextField(default ="Sudah Absen")
    Tanggal_absen = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username

class Absenstaff(models.Model):
    username = models.CharField(max_length=255)
    Absensi_status = models.TextField(default ="Sudah Absen")
    Tanggal_absen = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username

class Absen_rider(models.Model):
    Area = (
        ('Utara', 'Semarang Utara'),
        ('Barat', 'Semarang Barat'),
        ('Ngaliyan', 'Ngaliyan'),
        ('Tugu', 'Tugu'),
        ('Mijen', 'Mijen'),
    )    
    username = models.CharField(max_length=255)
    Absensi_status = models.TextField(default ="Sudah Absen")
    Arearider = models.CharField(max_length=30, choices=Area)
    J_paket = models.CharField(max_length=255)
    F_paket = models.CharField(max_length=255)
    Cod = models.CharField(max_length=255)
    Tanggal_absen = models.DateField(auto_now=True)

    def __str__(self):
        return self.username 

class Gaji(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE,limit_choices_to={'is_staff': False,'is_admin': False})
    p_miss = models.CharField(max_length=255, null=True, blank=True, default="0")
    p_qr = models.CharField(max_length=255, null=True, blank=True, default="0")
    parkir = models.CharField(max_length=255, null=True, blank=True, default="0")
    lembur = models.CharField(max_length=255, null=True, blank=True, default="0")
    asuransi = models.CharField(max_length=255, null=True, blank=True, default="0")
    Tanggal_absen = models.DateField(auto_now=True)

    def __str__(self):
        return self.username 



    
    