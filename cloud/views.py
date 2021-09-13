from users import views
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from private_storage.views import PrivateStorageDetailView

from .models import File, Folder, ShareFile


@login_required
def home(request):
    context = {}
    context['name'] = request.user.get_full_name()
    return render(request, 'cloud/home.html', context)


class DownloadFile(PrivateStorageDetailView):
    model = File
    model_file_field = 'file'

    def get_queryset(self):
        return super().get_queryset().filter(pk=self.kwargs['pk'])

    def can_access_file(self, private_file):
        # When the object can be accessed, the file may be downloaded.
        # This overrides PRIVATE_STORAGE_AUTH_FUNCTION
        try:
            if self.request.user.is_superuser:
                return True

            d_file = File.objects.get(pk=self.kwargs['pk'])
            if d_file:
                if d_file.user.pk == self.request.user.pk:
                    return True
                if ShareFile.objects.get(viewer=self.request.user, file=d_file):
                    return True
        except Exception as e:
            print(e)

        return False
