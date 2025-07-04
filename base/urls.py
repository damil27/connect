from django.urls import path
from . import views

urlpatterns = [
    path('login', views.loginPage, name='login'),  # Login page
    path('logout', views.logoutUser, name='logout'),  # Logout page
    path('register', views.registerUser, name='register'),  # Register page
    # path('', views.home, name='home'),  # Home page
    path("", views.room, name="room"),  # Room page
    path("details/<int:pk>", views.details, name="room_details"),  # Room page with primary key
    path("create_room", views.create_room, name="create_room"),  # Create room page
    path("update_room/<int:pk>", views.update_room, name="update_room"),  # Update room page
    path("delete_room/<int:pk>", views.delete_room, name="delete_room"),  # Delete room page
    path("delete_message/<int:pk>", views.delete_message, name="delete_message"),  # Delete room page
    path("user_profile/<int:pk>", views.userProfile, name="user_profile"),
    path("update_user", views.update_user, name='update_user')
]