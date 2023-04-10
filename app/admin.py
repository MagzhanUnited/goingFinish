from django.contrib import admin
from .models import Person, Message, Conversations

admin.site.register(Person)
admin.site.register(Message)
admin.site.register(Conversations)
