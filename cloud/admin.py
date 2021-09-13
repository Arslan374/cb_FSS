from django.contrib import admin

from .models import File, Folder, ShareFile


admin.site.register(Folder)
admin.site.register(File)
admin.site.register(ShareFile)
