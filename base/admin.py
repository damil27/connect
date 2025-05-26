from django.contrib import admin

# Register your models here.
from .models import Room, Topic, Message

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
# This code registers the Room model with the Django admin site, allowing it to be managed through the admin interface.