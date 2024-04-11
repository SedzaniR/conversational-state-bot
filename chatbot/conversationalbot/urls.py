from django.urls import path, include
from conversationalbot import views
from .api import (
    UserChatApiView,
)
urlpatterns = [
    path(r'login/',views.user_login,name='user_login'),
    path(r'api/chat/', UserChatApiView.as_view()),
    path(r'',views.conversation,name='conversation'),
]
