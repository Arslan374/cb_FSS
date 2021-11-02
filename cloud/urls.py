
from django.urls import path
from .views import (
    home,
    drive,
    file_upload,
    file_delete,
    file_rename,
    folder_create,
    folder_delete,
    folder_rename,
    share_view,
    share_file,
    share_get,
    share_remove,
    DownloadFile
)

urlpatterns = [
    path('', home, name='home'),
    path('drive/', drive, name='drive'),
    path('file/upload/', file_upload, name='file_upload'),
    path('file/delete/', file_delete, name='file_delete'),
    path('file/rename/', file_rename, name='file_rename'),


    path('share/', share_view, name='share_view'),
    path('share/get/', share_get, name='share_get'),
    path('share/file/', share_file, name='share_file'),
    path('share/remove/', share_remove, name='share_remove'),

    path('folder/create/', folder_create, name='folder_create'),
    path('folder/delete/', folder_delete, name='folder_delete'),
    path('folder/rename/', folder_rename, name='folder_rename'),

    path('file/dowload/<int:pk>/', DownloadFile.as_view(), name='file')
]
