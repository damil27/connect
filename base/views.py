from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Room, Topic, Message

from .forms import RoomForm, UserForm
from django.contrib.auth.models import User     
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# Create your views here.


def home(request):
        return render(request,"base/home.html")

def loginPage(request):
        page = 'login'
        if request.user.is_authenticated:
                return redirect('room')
        if request.method == 'POST':
                username = request.POST.get('username').lower()
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

        context = { 'page': page}
        return render(request, "base/login_register.html", context)

def logoutUser(request):
        logout(request)
        return redirect('room')
def registerUser(request):
        page = 'register'
        form  = UserCreationForm()
        if request.method == 'POST':
                form = UserCreationForm(request.POST)
                if form.is_valid():
                        user = form.save(commit=False)
                        user.username = user.username.lower()
                        user.save()
                        login(request, user)
                        return redirect('room')
                else:
                        messages.error(request, "An error occurred during registration")
        return render(request, "base/login_register.html", {'page': page, 'form': form})

def room(request):
        q = request.GET.get('q') if request.GET.get('q') != None else ''
        rooms = Room.objects.filter(
                Q(topic__name__icontains=q)| 
                Q(name__icontains=q) |
                Q(description__icontains=q)
                )
        topics =  Topic.objects.all()
        rooms_count = rooms.count()
        room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
        context =  {'rooms': rooms, 'topics': topics, 'rooms_count': rooms_count, 'room_messages':room_messages }
        return render(request,"base/room.html",context)

def details(request, pk):
        room = Room.objects.get(id=pk) 
        room_messages = room.message_set.all()
        participants = room.participants.all()
        print(participants)
        if request.method == 'POST':
                message = Message.objects.create(
                        user = request.user,
                        room = room,
                        body = request.POST.get('body')    
                )
                room.participants.add(request.user) 
                return redirect('room_details', pk=room.id)
        context = {'room': room, 'room_messages': room_messages, 'participants': participants}
        return render(request,"base/details.html", context)
# The above code defines three views for a Django application.
def userProfile(request, pk):
        user = User.objects.get(id=pk)
        rooms = user.room_set.all()
        room_messages = user.message_set.all()
        topics = Topic.objects.all()
        context = {"user":user, 'rooms': rooms, 'room_messages':room_messages, 'topics': topics}
        return render(request, "base/profile.html", context)
@login_required(login_url='login')
def create_room(request): 
        topics = Topic.objects.all()
        form = RoomForm()
        if request.method == 'POST':
                # print("Printing POST", request.POST)
                topic_name = request.POST.get('topic')
                topic, created = Topic.objects.get_or_create(name=topic_name)
                form = RoomForm(request.POST)
                Room.objects.create(
                         host = request.user,
                         topic = topic,
                         name = request.POST.get('name'),
                         description =  request.POST.get('description')
                )
                return redirect('room')

        context = {'form': form, 'topics': topics}
        return render(request, "base/create_room.html", context)

@login_required(login_url='login')
def update_room(request, pk):
        room =Room.objects.get(id=pk)
        form = RoomForm(instance=room)
        topics = Topic.objects.all()
        if room.host != request.user:
                return HttpResponse("You are not allowed here")
        if request.method == 'POST':
                topic_name = request.POST.get('topic')
                topic, created = Topic.objects.get_or_create(name=topic_name)
                room.name = request.POST.get('name')
                room.topic  = topic
                room.description = request.POST.get('description')
                room.save() 
                return redirect('room')
        # The above code defines a view for updating a room in a Django application.

        context = {'form': form, room: room,'topics':topics}
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

@login_required(login_url='login')
def delete_message(request, pk): 
        message  =  Message.objects.get(id=pk)
        if request.user != message.user:
                return HttpResponse("Your are not allowed here!!")
                
        if request.method == 'POST':
                message.delete()
                return redirect('room')
        
        return render(request, "base/delete.html", {'obj':message})
# The above code defines a view for deleting a room in a Django application.

def update_user(request):
        user = request.user
        form = UserForm(instance=user)

        if request.method == 'POST':
                form = UserForm(request.POST, instance=user)
                if form.is_valid():
                        form.save()
                        return redirect('user_profile', pk=user.id)
                else:
                        messages.error(request, "An error occurred during update")
        return render(request, 'base/update_user.html', {'form': form})