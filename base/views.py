from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room
from .forms import RoomForm
# Create your views here.


def home(request):
        return render(request,"base/home.html")

def room(request):
        rooms = Room.objects.all()
        return render(request,"base/room.html",{'rooms': rooms})

def details(request, pk):
        room = Room.objects.get(id=pk) 
        context = {'room': room}
        return render(request,"base/details.html", context)
# The above code defines three views for a Django application.

def create_room(request): 
        form = RoomForm()
        if request.method == 'POST':
                print("Printing POST", request.POST)
                form = RoomForm(request.POST)
                if form.is_valid():
                        form.save()

                        return redirect('room')

        context = {'form': form}
        return render(request, "base/create_room.html", context)


def update_room(request, pk):
        room =Room.objects.get(id=pk)
        form = RoomForm(instance=room)
        if request.method == 'POST':
                form = RoomForm(request.POST, instance=room)
                if form.is_valid():
                        print("Printing POST", request.POST)
                        form.save()
                        return redirect('room')
        # The above code defines a view for updating a room in a Django application.
                        



        context = {'form': form}
        return render(request, "base/create_room.html", context)