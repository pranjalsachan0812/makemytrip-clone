from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import TravelOption, Booking
from .forms import SignUpForm, BookingForm, UserForm, UserProfileForm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
import razorpay
from django.conf import settings


razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


@login_required
def initiate_payment(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    amount = int(booking.total_price * 100)  # amount in paise

    # Create Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount,
        currency='INR',
        payment_capture='1'
    ))

    booking.razorpay_order_id = razorpay_order['id']
    booking.save()

    context = {
        'booking': booking,
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'order_id': razorpay_order['id'],
        'amount': amount,
    }
    return render(request, 'payment.html', context)


@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id', '')
        order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')

        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        try:
            razorpay_client.utility.verify_payment_signature(params_dict)
        except razorpay.errors.SignatureVerificationError:
            return HttpResponseBadRequest("Payment verification failed")

        booking = get_object_or_404(Booking, razorpay_order_id=order_id)
        booking.status = 'Confirmed'
        booking.save()

        return render(request, 'payment_success.html')

    return HttpResponseBadRequest("Invalid request method")


@login_required
def payment_failure(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    return render(request, 'payment_failure.html', {'booking': booking})


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('travel_options')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


def travel_options(request):
    travel_type = request.GET.get('type')
    source = request.GET.get('source')
    destination = request.GET.get('destination')
    date = request.GET.get('date')

    options = TravelOption.objects.all()

    if travel_type:
        options = options.filter(type__iexact=travel_type)
    if source:
        options = options.filter(source__icontains=source)
    if destination:
        options = options.filter(destination__icontains=destination)
    if date:
        options = options.filter(date_time__date=date)

    context = {'travel_options': options}
    return render(request, 'travel_options.html', context)


@login_required
def book_travel(request, travel_id):
    travel_option = get_object_or_404(TravelOption, travel_id=travel_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            seats_requested = form.cleaned_data['number_of_seats']
            if seats_requested > travel_option.available_seats:
                form.add_error('number_of_seats', 'Not enough seats available')
            else:
                total_price = seats_requested * travel_option.price
                booking = Booking.objects.create(
                    user=request.user,
                    travel_option=travel_option,
                    number_of_seats=seats_requested,
                    total_price=total_price,
                    booking_date=timezone.now(),
                    status='Pending'  # Pending until payment success
                )
                travel_option.available_seats -= seats_requested
                travel_option.save()
                # Use booking.booking_id (not booking.id)
                return redirect('initiate_payment', booking_id=booking.booking_id)
    else:
        form = BookingForm()

    return render(request, 'book_travel.html', {'form': form, 'travel_option': travel_option})


@login_required
def view_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'view_bookings.html', {'bookings': bookings})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    if booking.status != 'Cancelled':
        booking.status = 'Cancelled'
        booking.save()

        # Update available seats on cancellation
        travel_option = booking.travel_option
        travel_option.available_seats += booking.number_of_seats
        travel_option.save()
    return redirect('view_bookings')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)

    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })
