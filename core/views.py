import datetime
import os
import csv
from urllib import response
from django.conf import settings
from io import BytesIO
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView, View
from django.db.models import Sum, Count
from django.contrib.staticfiles import finders
from django.template import loader

from .forms import (Absenfl_Form, AdduserForm, Captain_Form, CreateUserForm,
					LoginForm, Rider_Form, Staff_Form, Updatedata_Form,Gaji_form)
from .models import Absen_rider, Absencaptain, Absenfl_staff, Absenstaff,Gaji
from core import forms


"""form control"""

"""function control login"""

def LoginPage(request):
		form = LoginForm(request.POST or None)
		msg = None
		if request.method == 'POST':
			if form.is_valid():
				username = form.cleaned_data.get('username')
				password = form.cleaned_data.get('password')
				user = authenticate(username=username, password=password)
				if user is not None and user.is_admin:  # type: ignore
					login(request, user)
					return redirect('d_admin')
				elif user is not None and user.is_fl: # type: ignore
					login(request, user)
					return redirect('flpage')
				elif user is not None and user.is_captain: # type: ignore
					login(request, user)
					return redirect('captainpage')
				elif user is not None and user.is_staff: # type: ignore
					login(request, user)
					return redirect('staffpage')
				elif user is not None and user.is_rider: # type: ignore
					login(request, user)
					return redirect('riderpage')
				else:
					msg= 'invalid credentials'
			else:
				msg = 'error validating form'
		return render(request, 'login.html', {'form': form, 'msg': msg})


"""function control index"""
def index(request):
	return redirect('login')


"""function control logout"""
def LogoutUser(request):
	logout(request)
	return redirect('login')

"""function control biodata"""	

@login_required(login_url='login')
def BiodataPage(request):
		
	datafl = User.objects.all()

	context = {'datafl':datafl}

	return render(request, 'fl/biodata_fl.html', context)




"""function control signup"""
@login_required(login_url='login')
def Register(request):
	msg = None
	if request.method == 'POST':
		form = AdduserForm(request.POST)
		if form.is_valid():
			user = form.save()
			msg = 'user created'
			return redirect('d_admin')
		else:
			msg = 'form is not valid'
	else:
		form = AdduserForm()
	return render(request,'adminfl/signup.html', {'form': form, 'msg': msg})

@login_required(login_url='login')
def D_Flpage(request):
	user = get_user_model()
	current_datetime = datetime.datetime.today()
	form = Absenfl_Form()
	if request.method == "POST":
		form = Absenfl_Form(request.POST)
		if form.is_valid():
			form.save(commit = True)
		else:
			pass
		return redirect('sudahlogin')

	context = {'tanggal':current_datetime, 'form':form, 'user':user}
	return render(request, 'fl/d_fl.html', context)

@login_required(login_url='login')
def Datamp_page(request):
	user = get_user_model()
	datafl = user.objects.all()
	context = {'datafl':datafl}
	return render(request, 'adminfl/data_mp.html', context)

@login_required(login_url='login')
def Update_Datafl(request, username):  
	user = get_user_model()
	forms = user.objects.get(username=username)
	form = Updatedata_Form(request.POST, instance=forms)  
	if form.is_valid():  
		form.save()  
		return redirect("data_mp")  
	return render(request, 'adminfl/E_mp.html', {'form': form,'forms':forms})  

@login_required(login_url='login')
def Delete_Datafl(request, username):
	user = get_user_model()
	form = user.objects.get(username=username)
	form.delete()
	return redirect ("data_mp")


@login_required(login_url='login')
def AdminPage(request):
		current_datetime = datetime.datetime.today().date()
		absensi = Absen_rider.objects.filter(Tanggal_absen=current_datetime)
		j_fl = Absenfl_staff.objects.all().filter(Tanggal_absen=current_datetime).count() or 0
		j_captain = Absencaptain.objects.all().filter(Tanggal_absen=current_datetime).count() or 0
		j_staff = Absenstaff.objects.all().filter(Tanggal_absen=current_datetime).count() or 0
		j_rider = Absen_rider.objects.all().filter(Tanggal_absen=current_datetime).count() or 0
		j_pushout = Absen_rider.objects.filter(Tanggal_absen=current_datetime).aggregate(sum=Sum('J_paket'))['sum'] or 0
		j_fail = Absen_rider.objects.filter(Tanggal_absen=current_datetime).aggregate(sum=Sum('F_paket'))['sum'] or 0
		j_hold = Absencaptain.objects.filter(Tanggal_absen=current_datetime).aggregate(sum=Sum('J_hold'))['sum'] or 0
		j_cod = Absen_rider.objects.filter(Tanggal_absen=current_datetime).aggregate(sum=Sum('Cod'))['sum'] or 0.0
		p_mijen = absensi.filter(Arearider='Mijen',Tanggal_absen=current_datetime).aggregate(sum=Sum('J_paket'))['sum'] or 0
		p_tugu = absensi.filter(Arearider='Tugu',Tanggal_absen=current_datetime).aggregate(sum=Sum('J_paket'))['sum'] or 0
		p_ngaliyan = absensi.filter(Arearider='Ngaliyan',Tanggal_absen=current_datetime).aggregate(sum=Sum('J_paket'))['sum'] or 0
		p_barat = absensi.filter(Arearider='Barat',Tanggal_absen=current_datetime).aggregate(sum=Sum('J_paket'))['sum'] or 0
		p_utara = absensi.filter(Arearider='Utara',Tanggal_absen=current_datetime).aggregate(sum=Sum('J_paket'))['sum'] or 0

		context = {'j_fl':j_fl,'j_captain':j_captain,'j_staff':j_staff,'j_rider':j_rider,'j_pushout':j_pushout,
		'j_fail':j_fail,'j_hold':j_hold,'j_cod':j_cod,'p_mijen':p_mijen, 'p_tugu':p_tugu, 'p_ngaliyan':p_ngaliyan, 'p_barat':p_barat, 'p_utara':p_utara, }
		return render(request, 'adminfl/dashboardadmin.html', context)

@login_required(login_url='login')
def HomePage(request):
	return render(request, 'fl/index.html')

@login_required(login_url='login')  # type: ignore
def PaketPage(request):
	if request.user.is_authenticated:
					current_datetime = datetime.date.today()
					absensi = Absen_rider.objects.all()
					absensis =absensi.filter(Tanggal_absen=current_datetime)
					p_mijen = absensi.filter(Arearider='Mijen',Tanggal_absen=current_datetime)
					p_tugu = absensi.filter(Arearider='Tugu',Tanggal_absen=current_datetime)
					p_ngaliyan = absensi.filter(Arearider='Ngaliyan',Tanggal_absen=current_datetime)
					p_barat = absensi.filter(Arearider='Barat',Tanggal_absen=current_datetime)
					p_utara = absensi.filter(Arearider='Utara',Tanggal_absen=current_datetime)
					j_cod = absensis.aggregate(sum=Sum('Cod'))['sum'] or 0.00
					j_mijen = p_mijen.aggregate(sum=Sum('J_paket'))['sum'] or 0
					j_tugu = p_tugu.aggregate(sum=Sum('J_paket'))['sum'] or 0
					j_ngaliyan = p_ngaliyan.aggregate(sum=Sum('J_paket'))['sum'] or 0
					j_barat = p_barat.aggregate(sum=Sum('J_paket'))['sum'] or 0
					j_utara = p_utara.aggregate(sum=Sum('J_paket'))['sum'] or 0
					return render(request, 'adminfl/paket.html',{'absensi':absensi, 'j_mijen':j_mijen, 'j_tugu':j_tugu, 'j_ngaliyan':j_ngaliyan, 'j_barat':j_barat, 'j_utara':j_utara, 'j_cod':j_cod,})
	

def TestPage(request):
	return render(request, 'Test.html')	


"""function control fl page"""
@login_required(login_url='login')	
def FlPage(request):
	current_datetime = datetime.date.today()
	form = Absenfl_Form(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return redirect('sudahlogin')
		else:
			return redirect('flpage')
		

	return render(request, 'fl/index.html', {'tanggal':current_datetime,'form': form})

@login_required(login_url='login')
def Sudahloginfl(request):
	return render(request, 'fl/S_login.html')

@login_required(login_url='login')
def absenfl(request):
	form = Absenfl_Form(request.POST)
	if form.is_valid():
		form.save()
	else:
		return redirect('flpage')
	
	return render(request, 'sudahlogin') 

@login_required(login_url='login')
def HistoryPage(request):
	if request.user.is_authenticated:
		absensi = Absenfl_staff.objects.all()
		user = request.user
		absensis = absensi.filter(username=user)

		context = {'absensis':absensis}
		return render(request, 'fl/H_fl.html', context)
	else:
			return render(request, 'fl/H_fl.html')	


	


"""function control captain"""
@login_required(login_url='login')
def CaptainPage(request):
	current_datetime = datetime.date.today()
	form = Captain_Form(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return redirect('sudahlogincaptain')
		else:
			return redirect('captainpage')
		
	return render(request, 'captain/index.html', {'tanggal':current_datetime,'form': form})

@login_required(login_url='login')
def Sudahlogincaptain(request):
	return render(request, 'captain/S_login.html')

@login_required(login_url='login')
def HistorycaptainPage(request):
	if request.user.is_authenticated:
		absensi = Absencaptain.objects.all()
		user = request.user
		absensis = absensi.filter(username=user)
		context = {'absensis':absensis}
		return render(request, 'captain/H_captain.html', context)
	else:
			return render(request, 'captain/H_captain.html')	



	

"""function control staff"""

@login_required(login_url='login')
def StaffPage(request):
	current_datetime = datetime.date.today()
	form = Staff_Form(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return redirect('sudahloginstaff')
		else:
			return redirect('staffpage')
		
	return render(request, 'staff/index.html', {'tanggal':current_datetime,'form': form})

@login_required(login_url='login')
def Sudahloginstaff(request):
	return render(request, 'staff/S_login.html')

@login_required(login_url='login')
def HistorystaffPage(request):
	if request.user.is_authenticated:
		absensi = Absenstaff.objects.all()
		user = request.user
		absensis = absensi.filter(username=user)
		context = {'absensis':absensis}
		return render(request, 'staff/H_staff.html', context)
	else:
			return render(request, 'staff/H_staff.html')

@login_required(login_url='login')
def TambahgajiPage(request):
	current_datetime = datetime.date.today()
	form = Gaji_form(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return redirect('daftartambahgaji')
		else:
			return redirect('tambahgaji')
		
	return render(request, 'staff/addgaji.html', {'tanggal':current_datetime,'form': form})

@login_required(login_url='login')
def Daftartambahgaji(request):
	if request.user.is_authenticated:
		d_gaji = Gaji.objects.all()
		context = {'d_gaji':d_gaji}
		return render(request, 'staff/dt_gaji.html', context)
	else:
			return render(request, 'staff/H_staff.html')

@login_required(login_url='login')
def Printgajicsv(request):
	d_gaji = Gaji.objects.all()
	response = HttpResponse(
		content_type='text/csv',
		headers={'Content-Disposition': 'attachment; filename="datatambahgaji.csv"'},
	)

   
	t = loader.get_template('staff/basegaji.txt')
	c = {'data': d_gaji}
	response.write(t.render(c))
	return response



"""function control riderpage"""

@login_required(login_url='login')
def RiderPage(request):
	current_datetime = datetime.date.today()
	form = Rider_Form(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return redirect('sudahloginrider')
		else:
			return redirect('riderpage')
		
	return render(request, 'rider/index.html', {'tanggal':current_datetime,'form': form})

@login_required(login_url='login')
def Sudahloginrider(request):
	return render(request, 'rider/S_login.html')

@login_required(login_url='login')
def HistoryriderPage(request):
	if request.user.is_authenticated:
		absensi = Absen_rider.objects.all()
		user = request.user
		absensis = absensi.filter(username=user)
		context = {'absensis':absensis}
		return render(request, 'rider/H_rider.html', context)
	else:
		return render(request, 'rider/H_rider.html')
			

"""gaji page"""
@login_required(login_url='login')  # type: ignore
def GajiPage(request):
	if request.user.is_authenticated:
		user = get_user_model()
		data = user.objects.all().exclude(is_admin=True)
		context = {'datafl':data}
		return render(request, 'adminfl/gaji.html', context) # type: ignore


@login_required(login_url='login')  # type: ignore
def Detailgaji(request, username):
		user = get_user_model()
		forms = user.objects.get(username=username)
		if forms is not None and forms.is_rider: # type: ignore
				rider = Absen_rider.objects.all()
				dr_miss = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('p_miss'))['sum'] or 0
				dr_qr = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('p_qr'))['sum'] or 0
				dr_parkir = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('parkir'))['sum'] or 0
				dr_lembur = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('lembur'))['sum'] or 0
				dr_asuransi = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('asuransi'))['sum'] or 0
				d_rider = rider.filter(username=forms).aggregate(sum=Sum('J_paket'))['sum'] or 0
				gpaket = 1100

				g_rider = d_rider*gpaket
				td = g_rider+dr_parkir+dr_lembur+dr_asuransi
				tp = dr_qr+dr_miss
				ta = td-tp

				context = {'forms':forms,'gaji':g_rider,'dr_miss':dr_miss,'dr_qr':dr_qr,'dr_parkir':dr_parkir,
				'dr_lembur':dr_lembur,'dr_asuransi':dr_asuransi,'td':td,'tp':tp,'ta':ta,}

				return render(request, 'adminfl/detailgaji.html', context)
		elif forms is not None and forms.is_fl: # type: ignore
				freelance = Absenfl_staff.objects.all()
				dr_miss = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('p_miss'))['sum'] or 0
				dr_qr = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('p_qr'))['sum'] or 0
				dr_parkir = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('parkir'))['sum'] or 0
				dr_lembur = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('lembur'))['sum'] or 0
				dr_asuransi = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('asuransi'))['sum'] or 0
				a_fl = freelance.count()
				gfl = 108000

				d_fl = a_fl*gfl
				td = d_fl+dr_parkir+dr_lembur+dr_asuransi
				tp = dr_qr+dr_miss
				ta = td-tp

				context = {'forms':forms,'gaji':d_fl,'dr_miss':dr_miss,'dr_qr':dr_qr,'dr_parkir':dr_parkir,
				'dr_lembur':dr_lembur,'dr_asuransi':dr_asuransi,'td':td,'tp':tp,'ta':ta,}

				return render(request, 'adminfl/detailgaji.html', context)
		elif forms is not None and forms.is_captain: # type: ignore
				captain = Absencaptain.objects.all()
				dr_miss = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('p_miss'))['sum'] or 0
				dr_qr = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('p_qr'))['sum'] or 0
				dr_parkir = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('parkir'))['sum'] or 0
				dr_lembur = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('lembur'))['sum'] or 0
				dr_asuransi = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('asuransi'))['sum'] or 0
				a_c = captain.count()
				gc = 108000

				d_c = a_c*gc
				td = d_c+dr_parkir+dr_lembur+dr_asuransi
				tp = dr_qr+dr_miss
				ta = td-tp

				context = {'forms':forms,'gaji':d_c,'dr_miss':dr_miss,'dr_qr':dr_qr,'dr_parkir':dr_parkir,
				'dr_lembur':dr_lembur,'dr_asuransi':dr_asuransi,'td':td,'tp':tp,'ta':ta,}
				return render(request, 'adminfl/detailgaji.html', context)
		elif forms is not None and forms.is_staff: # type: ignore
				staff = Absenstaff.objects.all()
				dr_miss = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('p_miss'))['sum'] or 0
				dr_qr = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('p_qr'))['sum'] or 0
				dr_parkir = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('parkir'))['sum'] or 0
				dr_lembur = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('lembur'))['sum'] or 0
				dr_asuransi = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('asuransi'))['sum'] or 0
				a_s = staff.count()
				gs = 108000

				d_s = a_s*gs
				td = d_s+dr_parkir+dr_lembur+dr_asuransi
				tp = dr_qr+dr_miss
				ta = td-tp

				context = {'forms':forms,'gaji':d_s,'dr_miss':dr_miss,'dr_qr':dr_qr,'dr_parkir':dr_parkir,
				'dr_lembur':dr_lembur,'dr_asuransi':dr_asuransi,'td':td,'tp':tp,'ta':ta,}
				return render(request, 'adminfl/detailgaji.html', context)

def Downloadgaji(request, username):
		user = get_user_model()
		forms = user.objects.get(username=username)
		if forms is not None and forms.is_rider: # type: ignore
				rider = Absen_rider.objects.all()
				dr_miss = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('p_miss'))['sum'] or 0
				dr_qr = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('p_qr'))['sum'] or 0
				dr_parkir = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('parkir'))['sum'] or 0
				dr_lembur = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('lembur'))['sum'] or 0
				dr_asuransi = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('asuransi'))['sum'] or 0
				d_rider = rider.filter(username=forms).aggregate(sum=Sum('J_paket'))['sum'] or 0
				gpaket = 1100

				g_rider = d_rider*gpaket
				td = g_rider+dr_parkir+dr_lembur+dr_asuransi
				tp = dr_qr+dr_miss
				ta = td-tp
				template_path = 'adminfl/baseslip.html'
				context = {'forms':forms,'gaji':g_rider,'dr_miss':dr_miss,'dr_qr':dr_qr,'dr_parkir':dr_parkir,
				'dr_lembur':dr_lembur,'dr_asuransi':dr_asuransi,'td':td,'tp':tp,'ta':ta,}

				response = HttpResponse(content_type='application/pdf')
				response['Content-Disposition'] = 'filename="gaji.pdf"'

				template = get_template(template_path)
				html = template.render(context)

				# create a pdf
				pisa_status = pisa.CreatePDF(
				html, dest=response)
				# if error then show some funny view
				if pisa_status.err:  # type: ignore
					return HttpResponse('We had some errors <pre>' + html + '</pre>')
				return response

		elif forms is not None and forms.is_fl: # type: ignore
				freelance = Absenfl_staff.objects.all()
				dr_miss = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('p_miss'))['sum'] or 0
				dr_qr = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('p_qr'))['sum'] or 0
				dr_parkir = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('parkir'))['sum'] or 0
				dr_lembur = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('lembur'))['sum'] or 0
				dr_asuransi = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('asuransi'))['sum'] or 0
				a_fl = freelance.count()
				gfl = 108000

				d_fl = a_fl*gfl
				td = d_fl+dr_parkir+dr_lembur+dr_asuransi
				tp = dr_qr+dr_miss
				ta = td-tp
				template_path = 'adminfl/baseslip.html'
				context = {'forms':forms,'gaji':d_fl,'dr_miss':dr_miss,'dr_qr':dr_qr,'dr_parkir':dr_parkir,
				'dr_lembur':dr_lembur,'dr_asuransi':dr_asuransi,'td':td,'tp':tp,'ta':ta,}

				response = HttpResponse(content_type='application/pdf')
				response['Content-Disposition'] = 'filename="gaji.pdf"'

				template = get_template(template_path)
				html = template.render(context)

				# create a pdf
				pisa_status = pisa.CreatePDF(
				html, dest=response)
				# if error then show some funny view
				if pisa_status.err:  # type: ignore
					return HttpResponse('We had some errors <pre>' + html + '</pre>')
				return response
		elif forms is not None and forms.is_captain: # type: ignore
				captain = Absencaptain.objects.all()
				dr_miss = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('p_miss'))['sum'] or 0
				dr_qr = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('p_qr'))['sum'] or 0
				dr_parkir = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('parkir'))['sum'] or 0
				dr_lembur = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('lembur'))['sum'] or 0
				dr_asuransi = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('asuransi'))['sum'] or 0
				a_c = captain.count()
				gc = 108000
				d_c = a_c*gc
				td = d_c+dr_parkir+dr_lembur+dr_asuransi
				tp = dr_qr+dr_miss
				ta = td-tp

				template_path = 'adminfl/baseslip.html'
				context = {'forms':forms,'gaji':d_c,'dr_miss':dr_miss,'dr_qr':dr_qr,'dr_parkir':dr_parkir,
				'dr_lembur':dr_lembur,'dr_asuransi':dr_asuransi,'td':td,'tp':tp,'ta':ta,}

				response = HttpResponse(content_type='application/pdf')
				response['Content-Disposition'] = 'filename="gaji.pdf"'

				template = get_template(template_path)
				html = template.render(context)

				# create a pdf
				pisa_status = pisa.CreatePDF(
				html, dest=response)
				# if error then show some funny view
				if pisa_status.err:  # type: ignore
					return HttpResponse('We had some errors <pre>' + html + '</pre>')
				return response
		elif forms is not None and forms.is_staff: # type: ignore
				staff = Absenstaff.objects.all()
				dr_miss = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('p_miss'))['sum'] or 0
				dr_qr = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('p_qr'))['sum'] or 0
				dr_parkir = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('parkir'))['sum'] or 0
				dr_lembur = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('lembur'))['sum'] or 0
				dr_asuransi = Gaji.objects.all().filter(username=forms).aggregate(sum=Sum('asuransi'))['sum'] or 0
				a_s = staff.count()
				gs = 108000
				d_s = a_s*gs
				td = d_s+dr_parkir+dr_lembur+dr_asuransi
				tp = dr_qr+dr_miss
				ta = td-tp
				template_path = 'adminfl/baseslip.html'
				context = {'forms':forms,'gaji':d_s,'dr_miss':dr_miss,'dr_qr':dr_qr,'dr_parkir':dr_parkir,
				'dr_lembur':dr_lembur,'dr_asuransi':dr_asuransi,'td':td,'tp':tp,'ta':ta,}

				response = HttpResponse(content_type='application/pdf')
				response['Content-Disposition'] = 'filename="gaji.pdf"'

				template = get_template(template_path)
				html = template.render(context)

				# create a pdf
				pisa_status = pisa.CreatePDF(
				html, dest=response)
				# if error then show some funny view
				if pisa_status.err:  # type: ignore
					return HttpResponse('We had some errors <pre>' + html + '</pre>')
				return response

