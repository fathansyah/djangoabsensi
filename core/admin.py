from django.contrib import admin

from .models import Absen_rider, Absencaptain, Absenfl_staff, Absenstaff, Gaji, User

admin.site.register(User)

admin.site.register(Absenfl_staff)
admin.site.register(Absen_rider)
admin.site.register(Absencaptain)
admin.site.register(Absenstaff)
admin.site.register(Gaji)
