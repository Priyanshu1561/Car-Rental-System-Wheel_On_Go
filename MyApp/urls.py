from django.contrib import admin
from django.urls import path
from MyApp import views

urlpatterns = [
    path("", views.index, name='home'),
    path("home", views.index, name='home'),
    path("about", views.about, name='about'),
    path("vehicles", views.vehicles, name="vehicles"),
    path("register", views.register, name="register"),
    path("signin", views.signin, name="signin"),
    path("signout", views.signout, name="signout"),
    path("bill", views.bill, name="bill"),  # Use views.bill to render the bill page
    path("order", views.order, name="order"),  # Use views.order to handle the order processing
    path("contact", views.contact, name='contact'),

    # Razorpay payment routes
    path('initiate-payment/', views.initiate_payment, name='initiate_payment'),
    path('payment-callback/', views.payment_callback, name='payment_callback'),
]
