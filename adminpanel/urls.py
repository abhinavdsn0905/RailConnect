

from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [
    # Dashboard
    path('', views.admin_dashboard, name='dashboard'),

    # Users
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),

    # Trains
    path('trains/', views.train_list_admin, name='train_list'),
    path('trains/create/', views.train_create, name='train_create'),
    path('trains/<int:pk>/edit/', views.train_edit, name='train_edit'),
    path('trains/<int:pk>/delete/', views.train_delete, name='train_delete'),

    # Stations
    path('stations/', views.station_list, name='station_list'),
    path('stations/create/', views.station_create, name='station_create'),
    path('stations/<int:pk>/edit/', views.station_edit, name='station_edit'),
    path('stations/<int:pk>/delete/', views.station_delete, name='station_delete'),

    # Bookings
    path('bookings/', views.booking_list_admin, name='booking_list'),
    path('bookings/<int:pk>/delete/', views.booking_delete, name='booking_delete'),

    # PNR Lookup
    path('pnr/', views.pnr_lookup, name='pnr_lookup'),

    # Reports
    path('reports/', views.reports, name='reports'),
]