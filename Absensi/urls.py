from django.contrib import admin
from django.urls import path

from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', views.index, name="index"),
    path('', views.LoginPage, name='login'),
    path('logout/', views.LogoutUser, name='logout'),
    path('test/', views.TestPage, name='test'),

    path('home/', views.LoginPage, name='home'),   
    path('history/', views.HistoryPage, name='history'),
    path('biodata/', views.BiodataPage, name='biodata'),     

    path('register/', views.Register, name='register'),   
    path('d_fl/', views.D_Flpage, name='d_fl'),    
    path('data_mp/', views.Datamp_page, name='data_mp'),
    path('paket/', views.PaketPage, name='paket'),   
    path('gaji/', views.GajiPage, name='gaji'), 
    path('detailgaji/<str:username>', views.Detailgaji, name='detailgaji'),       
    path('delete/<str:username>', views.Delete_Datafl, name='delete'),   
    path('update/<str:username>', views.Update_Datafl, name='update'), 

    path('admindashboard/', views.AdminPage, name='d_admin'),   

    path('fldashboard/', views.FlPage, name='flpage'),
    path('s_login/', views.Sudahloginfl, name='sudahlogin'), 
    path('absenfl', views.absenfl, name='absenfl'),

    path('captaindashboard/', views.CaptainPage, name='captainpage'),
    path('s_logincaptain/', views.Sudahlogincaptain, name='sudahlogincaptain'),
    path('historycaptain/', views.HistorycaptainPage, name='historycaptain'),


    path('staffdashboard/', views.StaffPage, name='staffpage'), 
    path('s_loginstaff/', views.Sudahloginstaff, name='sudahloginstaff'),
    path('historystaff/', views.HistorystaffPage, name='historystaff'),
    path('tambahgaji/', views.TambahgajiPage, name='tambahgaji'),
    path('daftartambahangaji/', views.Daftartambahgaji, name='daftartambahgaji'),
    path('printgaji/', views.Printgajicsv, name='printgaji'),

    path('riderdashboard/', views.RiderPage, name='riderpage'), 
    path('s_loginrider/', views.Sudahloginrider, name='sudahloginrider'),
    path('historyrider/', views.HistoryriderPage, name='historyrider'),


    path('pdf_view/<str:username>', views.Downloadgaji, name="pdf_view"),  # type: ignore
    
    
]
