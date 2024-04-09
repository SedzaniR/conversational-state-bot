from django.urls import path, include
from conversationalbot import views
from .api import (
    UserChatApiView,
)
urlpatterns = [
    path(r'login/',views.user_login,name='user_login'),
    path(r'chat/', UserChatApiView.as_view()),
    path(r'conversation/',views.conversation,name='conversation'),
]
