from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from users.serializers import UserProfileSerializer

# Create your views here.
from rest_framework import generics, permissions
from .models import UserProfile
from .serializers import UserProfileSerializer

from rest_framework import generics
from .models import UserProfile
from .serializers import UserProfileSerializer

from rest_framework.exceptions import NotFound
from rest_framework.exceptions import AuthenticationFailed

from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from rest_framework import permissions, generics

class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Restrict access to only the profile of the authenticated user.
        """
        return UserProfile.objects.filter(user=self.request.user)

    def get_object(self):
        """
        Retrieve and validate the object for the authenticated user.
        """
        # Debugging: Print user and authorization details
        print("User:", self.request.user)
        print("Headers:", self.request.META.get("HTTP_AUTHORIZATION"))

        # Check if Authorization header exists
        auth_header = self.request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            raise AuthenticationFailed("Authorization header is missing.")

        # Ensure the user is authenticated
        if not self.request.user.is_authenticated:
            raise AuthenticationFailed("User is not authenticated.")

        # Fetch the object
        obj = super().get_object()

        # Ensure the user is authorized to access this profile
        if obj.user != self.request.user:
            raise PermissionDenied("You do not have permission to access this profile.")

        return obj




class UserRegistrationView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Debugging output
        print(f"Attempting to authenticate username: {username}, password: {password}")
        
        user = authenticate(username=username, password=password)
        if user:
            print(f"User authenticated: {user.username}, active: {user.is_active}")
            if not user.is_active:
                return Response({"detail": "Account is inactive"}, status=status.HTTP_400_BAD_REQUEST)
            return super().post(request, *args, **kwargs)
        
        print("Authentication failed.")
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)