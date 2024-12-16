from django.shortcuts import render
from rest_framework.permissions import AllowAny

# Create your views here.
from rest_framework import generics, filters, permissions
from .models import Job, Application
from .serializers import JobSerializer, ApplicationSerializer
from users.models import CustomUser

from rest_framework import generics, permissions, filters
from .models import Job
from .serializers import JobSerializer

class JobListView(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'location', 'salary']

    def get_permissions(self):
        if self.request.method == 'POST':
            # Only admin users can perform POST requests
            return [permissions.IsAdminUser()]
        # All other requests require authentication but not admin status
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            # Save with the user who created the job
            serializer.save(created_by=self.request.user)
        else:
            # If the user isn't authenticated, return an error
            raise permissions.exceptions.PermissionDenied("You must be logged in to create a job.")

class AddJobView(generics.CreateAPIView):
    """
    A view that allows only admin users to add (create) a job.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAdminUser]  # Only admin users can add jobs

    def perform_create(self, serializer):
        # Automatically assign the job to the logged-in admin user
        serializer.save(created_by=self.request.user)
class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class ApplicationView(generics.CreateAPIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access

    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserApplicationsView(generics.ListAPIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access

    serializer_class = ApplicationSerializer

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)

class AdminApplicationsView(generics.ListAPIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access

    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAdminUser]
