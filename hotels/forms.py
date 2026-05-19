from django import forms
from .models import Booking, Hotel, Room

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in', 'check_out']

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'location', 'description', 'image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check file size — max 2MB
            if image.size > 2 * 1024 * 1024:
                raise forms.ValidationError('Image size must be under 2MB')
            # Check file type
            if not image.name.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                raise forms.ValidationError('Only JPG, PNG and WEBP images are allowed')
        return image

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'room_type', 'price_per_night', 'is_available']