
from django.urls import path
from .views import (
    home,
    DownloadFile
)

urlpatterns = [
    path('', home, name='home'),
    path('file/<int:pk>/', DownloadFile.as_view(), name='file') 
]