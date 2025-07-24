from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import UserProfile  # optional
import json


@csrf_exempt
def api_register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        except:
            return JsonResponse({'detail': 'Invalid input'}, status=400)

        if not username or not password:
            return JsonResponse({'detail': 'Username and password required'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'detail': 'Username already exists'}, status=409)

        user = User.objects.create_user(username=username, password=password)
        login(request, user)

        # Optional: create user profile
        UserProfile.objects.get_or_create(user=user)

        return JsonResponse({'message': 'Registered successfully'})
    return JsonResponse({'detail': 'Only POST allowed'}, status=405)


@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")
        except:
            return JsonResponse({"detail": "Invalid input"}, status=400)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Optional: update last login
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.last_logged_in = timezone.now()
            profile.save()

            return JsonResponse({"message": "Login successful", "username": user.username})
        else:
            return JsonResponse({"detail": "Invalid credentials"}, status=401)
    return JsonResponse({"detail": "Only POST allowed"}, status=405)


@csrf_exempt
def api_logout(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({"message": "Logged out successfully"})
    return JsonResponse({"detail": "Only POST allowed"}, status=405)


@login_required
def api_home(request):
    return JsonResponse({"message": f"Welcome {request.user.username}!"})

