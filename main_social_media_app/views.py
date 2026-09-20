from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
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

        user = auth.authenticate(username=username, password=password)
        auth.login(request, user)

        user = User.objects.get(username = username)
        profile = Profile.objects.create(
            user=user, 
            profile_user_id=user.id,
            display_name=user.username
        )
        profile.save()
        return redirect('index')
    return render(request, 'register_form.html')

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is None:
            messages.error(request, "Username or password is incorrect. Please try again.")
            return redirect('login')
        auth.login(request, user)
        return redirect('index')
    return render(request, 'login_form.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def settings(request):

    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        bio = request.POST['bio']
        location = request.POST['location']
        website = request.POST['website']

        if request.FILES.get('avatar') == None:
            avatar = request.user.avatar
        else: 
            avatar = request.FILES.get('avatar')

        request.user.username = username
        profile.display_name = username
        request.user.email = email
        profile.bio = bio
        profile.location = location
        profile.website = website
        profile.avatar = avatar

        request.user.save()
        profile.save()

        return redirect('settings')
    
    return render(request, 'setting.html', {
        'profile': profile,
        'user': request.user
    })