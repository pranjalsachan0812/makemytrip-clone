from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import initiate_payment, payment_success, payment_failure

urlpatterns = [
    path('', views.travel_options, name='home'),  # root URL points to travel options
    path('register/', views.register, name='register'),
    path('travel-options/', views.travel_options, name='travel_options'),
    path('book/<int:travel_id>/', views.book_travel, name='book_travel'),
    path('my-bookings/', views.view_bookings, name='view_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('payment/<int:booking_id>/', initiate_payment, name='initiate_payment'),
    path('payment/success/', payment_success, name='payment_success'),
    path('payment/failure/<int:booking_id>/', payment_failure, name='payment_failure'),
]
