from django.urls import path
from .views import VideoStreamAPIView

urlpatterns = [
    path('stream/<int:video_id>/', VideoStreamAPIView.as_view(), name='video_stream'),
]