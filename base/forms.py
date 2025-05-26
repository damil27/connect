from django.forms import ModelForm
from .models import Room, Message

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = [ 'host','topic','name', 'description']