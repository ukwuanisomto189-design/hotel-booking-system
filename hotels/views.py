from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Hotel, Room, Booking
from .forms import BookingForm, HotelForm, RoomForm
from datetime import date

def index(request):
    query = request.GET.get('q', '')
    location = request.GET.get('location', '')
    hotels = Hotel.objects.all()
    if query:
        hotels = hotels.filter(name__icontains=query)
    if location:
        hotels = hotels.filter(location__icontains=location)
    return render(request, 'hotels/index.html', {'hotels': hotels, 'query': query, 'location': location})

@login_required
def hotel_detail(request, hotel_id):
    hotel = Hotel.objects.get(id=hotel_id)
    rooms = Room.objects.filter(hotel=hotel)
    return render(request, 'hotels/hotel_detail.html', {'hotel': hotel, 'rooms': rooms})

@login_required
def book_room(request, room_id):
    room = Room.objects.get(id=room_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']
            # Validate dates
            if check_in < date.today():
                form.add_error('check_in', 'Check in date cannot be in the past')
            elif check_out <= check_in:
                form.add_error('check_out', 'Check out date must be after check in date')
            else:
                # Check if room is already booked for those dates
                existing_booking = Booking.objects.filter(
                    room=room,
                    check_in__lt=check_out,
                    check_out__gt=check_in
                ).exists()

                if existing_booking:
                    form.add_error(None, 'Sorry! This room is already booked for those dates. Please choose different dates.')
                else:
                    booking = form.save(commit=False)
                    booking.room = room
                    booking.user = request.user
                    number_of_nights = (check_out - check_in).days
                    booking.total_price = room.price_per_night * number_of_nights
                    booking.save()
                    return redirect('my_bookings')
    else:
        form = BookingForm()
    return render(request, 'hotels/book_room.html', {'form': form, 'room': room})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'hotels/my_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if booking.user == request.user:
        booking.delete()
    return redirect('my_bookings')

@login_required
def add_hotel(request):
    if not request.user.is_staff:
        return redirect('index')
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)
        if form.is_valid():
            hotel = form.save(commit=False)
            hotel.created_by = request.user
            hotel.save()
            return redirect('index')
    else:
        form = HotelForm()
    return render(request, 'hotels/add_hotel.html', {'form': form})

@login_required
def edit_hotel(request, hotel_id):
    if not request.user.is_staff:
        return redirect('index')
    hotel = Hotel.objects.get(id=hotel_id)
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES, instance=hotel)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = HotelForm(instance=hotel)
    return render(request, 'hotels/edit_hotel.html', {'form': form, 'hotel': hotel})

@login_required
def delete_hotel(request, hotel_id):
    if not request.user.is_staff:
        return redirect('index')
    hotel = Hotel.objects.get(id=hotel_id)
    hotel.delete()
    return redirect('index')

@login_required
def add_room(request, hotel_id):
    if not request.user.is_staff:
        return redirect('index')
    hotel = Hotel.objects.get(id=hotel_id)
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.hotel = hotel
            room.save()
            return redirect('hotel_detail', hotel_id=hotel_id)
    else:
        form = RoomForm()
    return render(request, 'hotels/add_room.html', {'form': form, 'hotel': hotel})

@login_required
def edit_room(request, room_id):
    if not request.user.is_staff:
        return redirect('index')
    room = Room.objects.get(id=room_id)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('hotel_detail', hotel_id=room.hotel.id)
    else:
        form = RoomForm(instance=room)
    return render(request, 'hotels/edit_room.html', {'form': form, 'room': room})

@login_required
def delete_room(request, room_id):
    if not request.user.is_staff:
        return redirect('index')
    room = Room.objects.get(id=room_id)
    hotel_id = room.hotel.id
    room.delete()
    return redirect('hotel_detail', hotel_id=hotel_id)