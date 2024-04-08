from django.urls import path, include
from conversationalbot import views

urlpatterns = [
    path(r'chat/',views.chat,name='chat')
]
