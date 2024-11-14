from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import User

@login_required
def User_Profile(request):
    user = request.user

    if user.user_type == "farmer":
        user.user_status = "חקלאי"
    else:
        user.user_status = "עובד"

    context = {"user": user}

    return render(request, 'users/user_profile.html', context)