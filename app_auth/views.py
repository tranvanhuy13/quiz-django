from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.utils import timezone
from .models import UserProfile  # optional


from rest_framework.permissions import AllowAny


class UserAuthViewSet(ViewSet):
    authentication_classes = []  # No authentication required for registration and login
    permission_classes = [AllowAny]

    @action(detail=False, methods=["post"], url_path="register")
    def register(self, request):
        data = request.data
        username = data.get("username")
        password = data.get("password")
        role = data.get("role", "Student")  # Default role is Student
        if not username or not password:
            return Response(
                {"detail": "Username and password required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if role not in ["Teacher", "Student"]:
            return Response(
                {"detail": "Invalid role"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if User.objects.filter(username=username).exists():
            return Response(
                {"detail": "Username already exists"}, status=status.HTTP_409_CONFLICT
            )
        user = User.objects.create_user(username=username, password=password)

        group, _ = Group.objects.get_or_create(name=role)
        user.groups.add(group)

        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.role = role
        profile.save()

        login(request, user)
        return Response(
            {"message": "Registered successfully"}, status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=["post"], url_path="login")
    def login_view(self, request):
        data = request.data
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return Response(
                {"detail": "Username and password required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.last_logged_in = timezone.now()
            profile.save()
            return Response(
                {"message": "Login successful", "username": user.username},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

    @action(detail=False, methods=["post"], url_path="logout")
    def logout_view(self, request):
        logout(request)
        return Response(
            {"message": "Logged out successfully"}, status=status.HTTP_200_OK
        )
