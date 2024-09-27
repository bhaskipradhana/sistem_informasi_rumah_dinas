from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('laporan/create/', views.create_laporan, name='create_laporan'),
    path('laporan/', views.list_laporan, name='list_laporan'),
    path('laporan/approve/<int:pk>/', views.approve_laporan, name='approve_laporan'),
    path('laporan/reject/<int:pk>/', views.reject_laporan, name='reject_laporan'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('laporan/update/<int:pk>/', views.update_laporan, name='update_laporan'),
    path('laporan/view/<int:pk>/', views.view_laporan, name='view_laporan'),
    path('laporan/delete/<int:pk>/', views.delete_laporan, name='delete_laporan'),
    path('approver/jadwal-perbaikan/', views.jadwal_perbaikan, name='jadwal_perbaikan'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
