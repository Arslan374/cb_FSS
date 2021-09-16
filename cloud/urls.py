
from django.urls import path
from .views import (
    home,
    drive,
    file_upload,
    file_delete,
    DownloadFile
)

urlpatterns = [
    path('', home, name='home'),
    path('drive/', drive, name='drive'),
    path('file/upload/', file_upload, name='file_upload'),
    path('file/delete/', file_delete, name='file_delete'),
    path('file/dowload/<int:pk>/', DownloadFile.as_view(), name='file')
]
