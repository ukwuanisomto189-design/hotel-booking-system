from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hotels/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    path('book/<int:room_id>/', views.book_room, name='book_room'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('add-hotel/', views.add_hotel, name='add_hotel'),
    path('edit-hotel/<int:hotel_id>/', views.edit_hotel, name='edit_hotel'),
    path('delete-hotel/<int:hotel_id>/', views.delete_hotel, name='delete_hotel'),
    path('add-room/<int:hotel_id>/', views.add_room, name='add_room'),
    path('edit-room/<int:room_id>/', views.edit_room, name='edit_room'),
    path('delete-room/<int:room_id>/', views.delete_room, name='delete_room'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]