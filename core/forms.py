from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import Absen_rider, Absencaptain, Absenfl_staff, Absenstaff, User, Gaji


class Absenfl_Form(ModelForm):
	class Meta:
		model = Absenfl_staff
		fields = ['username']
        
        
class Staff_Form(ModelForm):
	class Meta:
		model = Absenstaff
		fields = ['username']

class Captain_Form(ModelForm):
	class Meta:
		model = Absencaptain
		fields = ['username','J_hold']	

class Rider_Form(ModelForm):
	class Meta:
		model = Absen_rider
		fields = ['username','Arearider','J_paket','F_paket','Cod']

class CreateUserForm(UserCreationForm.Meta):
	class Meta:
		model = User
		fields = UserCreationForm.Meta.fields + ('kodehub', 'telp', 'nik', 'branch', 'role', 'is_admin', 'is_fl', 'is_captain','is_staff','is_rider')  # type: ignore


class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )

class AdduserForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    branch = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    nik = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    telp = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    kodehub = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2','branch','nik','telp','kodehub', 'is_admin', 'is_fl', 'is_captain','is_staff','is_rider')


class Updatedata_Form(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    branch = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    nik = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    telp = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    kodehub = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2','branch','nik','telp','kodehub', 'is_admin', 'is_fl', 'is_captain','is_staff','is_rider')

class Gaji_form(ModelForm):
    	class Meta:
            model = Gaji
            fields = ['username','p_miss','p_qr','parkir','lembur','asuransi',]