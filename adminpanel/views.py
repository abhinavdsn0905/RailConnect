

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
import json

from user.models import User
from trains.models import Train, Station
from bookings.models import Booking



def is_admin(request):
    """Check if logged-in user is admin"""
    username = request.session.get('username')
    if not username:
        return False
    # You can add admin check logic here
    # For now, any logged-in user can access admin panel
    return True


# DASHBOARD VIEW

def admin_dashboard(request):
    if not is_admin(request):
        return redirect('login')

    today = timezone.now().date()

    # Calculate stats
    total_users = User.objects.count()
    active_trains = Train.objects.filter(status='on_time').count()
    today_bookings = Booking.objects.filter(travel_date=today).count()
    total_revenue = Booking.objects.aggregate(total=Sum('total_price'))['total'] or 0

    # Weekly booking data for chart (last 7 days)
    weekly_data = []
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        count = Booking.objects.filter(travel_date=date).count()
        weekly_data.append(count)

    # Recent bookings
    recent_bookings = Booking.objects.all()

    # Train occupancy
    train_occupancy = Train.objects.all()[:5]

    context = {
        'total_users': total_users,
        'active_trains': active_trains,
        'today_bookings': today_bookings,
        'total_revenue': total_revenue,
        'weekly_data': weekly_data,
        'recent_bookings': recent_bookings,
        'train_occupancy': train_occupancy,
    }
    return render(request, 'adminpanel/dashboard.html', context)



# USER MANAGEMENT

def user_list(request):
    if not is_admin(request):
        return redirect('login')

    query = request.GET.get('q', '')
    users = User.objects.all()
    users_with_counts = []
    for user in users:
        booking_count = Booking.objects.filter(username=user.username).count()
        users_with_counts.append((user, booking_count))

    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query)
        )

    return render(request, 'adminpanel/users.html', {
        'users': users,
        'query': query,
    })


def user_create(request):
    if not is_admin(request):
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=403)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = User.objects.create(
                username=data['username'],
                email=data['email'],
                password=data['password'],  # In production, hash this!
            )
            return JsonResponse({'success': True, 'id': user.id, 'message': 'User created successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


def user_edit(request, pk):
    if not is_admin(request):
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=403)

    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            user.save()
            return JsonResponse({'success': True, 'message': 'User updated successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    # GET: return user data
    return JsonResponse({
        'id': user.id,
        'username': user.username,
        'email': user.email,
    })


def user_delete(request, pk):
    if not is_admin(request):
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=403)

    if request.method == 'DELETE':
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return JsonResponse({'success': True, 'message': 'User deleted'})

    return JsonResponse({'success': False}, status=400)



# TRAIN MANAGEMENT

def train_list_admin(request):
    if not is_admin(request):
        return redirect('login')

    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    trains = Train.objects.all()

    if query:
        trains = trains.filter(
            Q(train_name__icontains=query) |
            Q(train_number__icontains=query) |
            Q(source__icontains=query) |
            Q(destination__icontains=query)
        )
    if status:
        trains = trains.filter(status=status)

    return render(request, 'adminpanel/trains.html', {
        'trains': trains,
        'query': query,
        'status': status,
    })


def train_create(request):
    if not is_admin(request):
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=403)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            train = Train.objects.create(
                train_number=data['train_number'],
                train_name=data['train_name'],
                source=data['source'],
                destination=data['destination'],
                departure_time=data['departure_time'],
                arrival_time=data['arrival_time'],
                total_seats=data['total_seats'],
                available_seats=data['total_seats'],
                price=data.get('price', 500),
                status=data.get('status', 'on_time'),
            )
            return JsonResponse({'success': True, 'id': train.id, 'message': 'Train added successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    return JsonResponse({'success': False}, status=400)


def train_edit(request, pk):
    if not is_admin(request):
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=403)

    train = get_object_or_404(Train, pk=pk)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            train.train_name = data.get('train_name', train.train_name)
            train.departure_time = data.get('departure_time', train.departure_time)
            train.arrival_time = data.get('arrival_time', train.arrival_time)
            train.total_seats = data.get('total_seats', train.total_seats)
            train.available_seats = data.get('available_seats', train.available_seats)
            train.status = data.get('status', train.status)
            train.price = data.get('price', train.price)
            train.save()
            return JsonResponse({'success': True, 'message': 'Train updated'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    # GET: return train data
    return JsonResponse({
        'id': train.id,
        'train_number': train.train_number,
        'train_name': train.train_name,
        'source': train.source,
        'destination': train.destination,
        'departure_time': str(train.departure_time),
        'arrival_time': str(train.arrival_time),
        'total_seats': train.total_seats,
        'available_seats': train.available_seats,
        'status': train.status,
        'price': train.price,
    })


def train_delete(request, pk):
    if not is_admin(request):
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=403)

    if request.method == 'DELETE':
        train = get_object_or_404(Train, pk=pk)
        train.delete()
        return JsonResponse({'success': True, 'message': 'Train deleted'})

    return JsonResponse({'success': False}, status=400)



# STATION MANAGEMENT

def station_list(request):
    if not is_admin(request):
        return redirect('login')

    query = request.GET.get('q', '')
    stations = Station.objects.all()

    if query:
        stations = stations.filter(
            Q(name__icontains=query) |
            Q(code__icontains=query) |
            Q(city__icontains=query) |
            Q(state__icontains=query)
        )

    return render(request, 'adminpanel/stations.html', {
        'stations': stations,
        'query': query,
    })


def station_create(request):
    if not is_admin(request):
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=403)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            station = Station.objects.create(
                code=data['code'].upper(),
                name=data['name'],
                city=data['city'],
                state=data['state'],
                platforms=data.get('platforms', 1),
            )
            return JsonResponse({'success': True, 'id': station.id, 'message': 'Station added'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    return JsonResponse({'success': False}, status=400)


def station_edit(request, pk):
    if not is_admin(request):
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=403)

    station = get_object_or_404(Station, pk=pk)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            station.name = data.get('name', station.name)
            station.city = data.get('city', station.city)
            station.state = data.get('state', station.state)
            station.platforms = data.get('platforms', station.platforms)
            station.save()
            return JsonResponse({'success': True, 'message': 'Station updated'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    return JsonResponse({
        'id': station.id, 'code': station.code, 'name': station.name,
        'city': station.city, 'state': station.state, 'platforms': station.platforms,
    })


def station_delete(request, pk):
    if not is_admin(request):
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=403)

    if request.method == 'DELETE':
        station = get_object_or_404(Station, pk=pk)
        station.delete()
        return JsonResponse({'success': True, 'message': 'Station deleted'})

    return JsonResponse({'success': False}, status=400)



# BOOKING MANAGEMENT

def booking_list_admin(request):
    if not is_admin(request):
        return redirect('login')

    query = request.GET.get('q', '')
    bookings = Booking.objects.select_related('train').order_by('-id')

    if query:
        bookings = bookings.filter(
            Q(pnr__icontains=query) |
            Q(username__icontains=query)
        )

    return render(request, 'adminpanel/bookings.html', {
        'bookings': bookings,
        'query': query,
    })


def booking_delete(request, pk):
    if not is_admin(request):
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=403)

    if request.method == 'DELETE':
        booking = get_object_or_404(Booking, pk=pk)
        # Restore seats
        booking.train.available_seats += booking.passengers
        booking.train.save()
        booking.delete()
        return JsonResponse({'success': True, 'message': 'Booking deleted'})

    return JsonResponse({'success': False}, status=400)



# PNR LOOKUP

def pnr_lookup(request):
    if not is_admin(request):
        return JsonResponse({'found': False, 'message': 'Unauthorized'}, status=403)

    pnr = request.GET.get('pnr', '').strip().upper()
    if not pnr:
        return JsonResponse({'found': False, 'message': 'PNR is required'})

    try:
        booking = Booking.objects.select_related('train').get(pnr=pnr)
        return JsonResponse({
            'found': True,
            'pnr': booking.pnr,
            'passenger': booking.username,
            'train': booking.train.train_name,
            'train_number': booking.train.train_number,
            'from': booking.train.source,
            'to': booking.train.destination,
            'date': str(booking.travel_date),
            'seats': booking.passengers,
            'amount': str(booking.total_price),
            'status': 'Confirmed',
        })
    except Booking.DoesNotExist:
        return JsonResponse({'found': False, 'message': f'PNR {pnr} not found'})



# REPORTS

def reports(request):
    if not is_admin(request):
        return redirect('login')

    today = timezone.now().date()

    # Stats
    total_bookings = Booking.objects.count()
    total_revenue = Booking.objects.aggregate(total=Sum('total_price'))['total'] or 0

    # Top routes
    top_routes = (
        Booking.objects
        .values('train__source', 'train__destination')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )

    context = {
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'top_routes': top_routes,
    }
    return render(request, 'adminpanel/reports.html', context)