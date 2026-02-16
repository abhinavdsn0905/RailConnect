from django.shortcuts import render, redirect, get_object_or_404
from trains.models import Train
from django.conf import settings
from .models import Booking 
from django.core.mail import send_mail
from user.models import User

def booking_page(request):
    if not request.session.get("username"):
        return redirect("login")

    return render(request, "booking.html")


def book_train(request, train_id):
    if not request.session.get("username"):
        return redirect("login")

    train = get_object_or_404(Train, id=train_id)
    username = request.session.get("username")

    if train.available_seats <= 0:
        return redirect("train_list")

    # create booking
    Booking.objects.create(
        username=username,
        train=train,
        seats_booked=1
    )

    # reduce seat
    train.available_seats -= 1
    train.save()

    # get user email
    user = User.objects.get(username=username)

    # send confirmation email
    send_mail(
        "Train Booking Confirmation",
        f"Hello {username},\n\n"
        f"Your booking for {train.train_name} "
        f"from {train.source} to {train.destination} "
        f"is confirmed.\n\n"
        f"Departure: {train.departure_time}\n"
        f"Arrival: {train.arrival_time}\n"
        f"Price: ₹{train.price}\n\n"
        f"Thank you for booking with RailConnect!",
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )

    return redirect("train_list")


def my_bookings(request):
    if not request.session.get("username"):
        return redirect("login")

    username = request.session.get("username")

    bookings = Booking.objects.filter(username=username)

    return render(request, "my_bookings.html", {"bookings": bookings})