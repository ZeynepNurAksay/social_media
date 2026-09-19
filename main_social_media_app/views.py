from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirmation = request.POST['password_confirmation']

        if password != password_confirmation:
            messages.error(request, "Passwords do not match!")
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, "An accoung with this email already exists. Please try another email address.")
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request, "An accoung with this username already exists. Please try another username.")
            return redirect('register')
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        user = User.objects.get(username = username)
        profile = Profile.objects.create(
            user=user, 
            profile_user_id=user.id,
            display_name=user.username
        )
        profile.save()
        return redirect('index')
    return render(request, 'register_form.html')