from django.urls import path
from .views import JobListView, JobDetailView, ApplicationView, UserApplicationsView, AdminApplicationsView, AddJobView

urlpatterns = [
    path('jobs/', JobListView.as_view(), name='job-list'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('apply/', ApplicationView.as_view(), name='apply-job'),
    path('jobs/add/', AddJobView.as_view(), name='add-job'),         # Add a new job
    path('user/applications/', UserApplicationsView.as_view(), name='user-applications'),
    path('admin/applications/', AdminApplicationsView.as_view(), name='admin-applications'),
]
