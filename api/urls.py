 
from django.urls import path, include
from .views import HomeAPIView

urlpatterns = [
    path('home/', HomeAPIView.as_view(), name='home'),
    # Add more API endpoints as needed
]