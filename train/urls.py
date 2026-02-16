"""
URL configuration for train project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user import views as user_views
from trains import views as train_views
from bookings import views as booking_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # user pages
    path('', user_views.landing, name='landing'),
    path('register/', user_views.register, name='register'),
    path('login/', user_views.login, name='login'),
    path('logout/', user_views.logout, name='logout'),

    # train pages
    path('trains/', train_views.train_list, name='train_list'),

    # booking
    path('book/<int:train_id>/', booking_views.book_train, name='book_train'),
    path('my-bookings/', booking_views.my_bookings, name='my_bookings'),
]
