
from django.urls import path
from .views import (
    home,
    drive,
    file_upload,
    DownloadFile
)

urlpatterns = [
    path('', home, name='home'),
    path('drive/', drive, name='drive'),
    path('file/upload/', file_upload, name='file_upload'),
    path('file/<int:pk>/', DownloadFile.as_view(), name='file')
]
