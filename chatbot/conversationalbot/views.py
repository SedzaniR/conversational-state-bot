from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
import json



def register(request):
    pass

def user_login(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("conversationalbot:conversation")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "registration/login.html")


@login_required
def conversation(request):

    user = request.user
    if not user:
        return redirect("conversationalbot:user_login")
    user_logs = list(user.log_set.all().values("user_input", "bot_response","created_at"))
    context = {"user_logs": user_logs}
    return render(request, "chat.html", context=context)


# Create your views here.
