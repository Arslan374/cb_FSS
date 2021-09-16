
from django.urls import path
from .views import (
    home,
    drive, 
    DownloadFile
)

urlpatterns = [
    path('', home, name='home'),
    path('drive/', drive, name='drive'),
    path('file/<int:pk>/', DownloadFile.as_view(), name='file') 
]