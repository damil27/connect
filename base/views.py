from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Room, Topic

from .forms import RoomForm
from django.contrib.auth.models import User     
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.


def home(request):
        return render(request,"base/home.html")

def loginPage(request):
        if request.user.is_authenticated:
                return redirect('room')
        if request.method == 'POST':
                username = request.POST.get('username')
                password = request.POST.get('password')
                try:
                        user = User.objects.get(username=username)
                except:
                        messages.error(request, "User does not exist")
                        # return render(request, "base/login_register.html") 
                user = authenticate(request, username=username, password=password)
                if user is not None:
                        login(request, user)
                        return redirect('room')
                else:
                        messages.error(request, "Username or password is incorrect")
                        # return render(request, "base/login_register.html")

        contenxt = {}
        return render(request, "base/login_register.html", contenxt)

def logoutUser(request):
        logout(request)
        return redirect('home')

def room(request):
        q = request.GET.get('q') if request.GET.get('q') != None else ''
        rooms = Room.objects.filter(
                Q(topic__name__icontains=q)| 
                Q(name__icontains=q) |
                Q(description__icontains=q)
                )
        topics =  Topic.objects.all()
        rooms_count = rooms.count()
        context =  {'rooms': rooms, 'topics': topics, 'rooms_count': rooms_count}
        return render(request,"base/room.html",context)

def details(request, pk):
        room = Room.objects.get(id=pk) 
        context = {'room': room}
        return render(request,"base/details.html", context)
# The above code defines three views for a Django application.

@login_required(login_url='login')
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

@login_required(login_url='login')
def update_room(request, pk):
        room =Room.objects.get(id=pk)
        form = RoomForm(instance=room)
        if room.host != request.user:
                return HttpResponse("You are not allowed here")
        if request.method == 'POST':
                form = RoomForm(request.POST, instance=room)
                if form.is_valid():
                        print("Printing POST", request.POST)
                        form.save()
                        return redirect('room')
        # The above code defines a view for updating a room in a Django application.

        context = {'form': form}
        return render(request, "base/create_room.html", context)

@login_required(login_url='login')
def delete_room(request, pk): 
        room  =  Room.objects.get(id=pk)
        form = RoomForm(instance=room)
        if request.method == 'POST':
                room.delete()
                return redirect('room')
        
        return render(request, "base/delete.html", {'obj':room})
# The above code defines a view for deleting a room in a Django application.