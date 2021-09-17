
from django.urls import path
from .views import (
    home,
    drive,
    file_upload,
    file_delete,
    folder_create,
    folder_delete,
    share_file,
    share_remove,
    DownloadFile
)

urlpatterns = [
    path('', home, name='home'),
    path('drive/', drive, name='drive'),
    path('file/upload/', file_upload, name='file_upload'),
    path('file/delete/', file_delete, name='file_delete'),

    path('share/file/', share_file, name='share_file'),
    path('share/remove/', share_remove, name='share_remove'),

    path('folder/create/', folder_create, name='folder_create'),
    path('folder/delete/', folder_delete, name='folder_delete'),
    path('file/dowload/<int:pk>/', DownloadFile.as_view(), name='file')
]
