from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProfileForm

def login_view(request):
    # Pre-set credentials
    DEFAULT_USERNAME = "SwapMeTester"
    DEFAULT_PASSWORD = "Tester2025!"
    
    # Create the demo user if it doesn't exist
    if not User.objects.filter(username=DEFAULT_USERNAME).exists():
        User.objects.create_user(
            username=DEFAULT_USERNAME,
            password=DEFAULT_PASSWORD
        )
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")
            return redirect("feed")
        messages.error(request, "Invalid username or password")
    
    # Pass default username to template for convenience
    return render(request, "accounts/login.html", {
        "username": DEFAULT_USERNAME
    })

def success_view(request):
    return render(request, "accounts/success.html")

def logout_view(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def edit_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("my_stall")
    else:
        form = ProfileForm(instance=request.user)
    
    return render(request, "accounts/edit_profile.html", {"form": form})
