import os
import time
from users import views
from django.contrib import messages
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

from private_storage.views import PrivateStorageDetailView

from .models import File, Folder, ShareFile


@login_required
def home(request):
    if request.user.is_superuser:
        context = {}
        context['name'] = request.user.get_full_name()
        return render(request, 'cloud/home.html', context)
    return redirect('/drive/')


@login_required
def drive(request):
    context = {}
    folder_id = int(request.GET.get('id', 0))

    current_folder = Folder.objects.filter(user=request.user, id=folder_id)
    top_dir = Folder.objects.get(user=request.user, depth=0)
    if current_folder.exists():
        current_folder = current_folder.first()
    else:
        current_folder = top_dir
    top_dir = model_to_dict(top_dir)
    top_dir['name'] = "Home"
    files = File.objects.filter(user=request.user, folder=current_folder)
    folders = Folder.objects.filter(
        user=request.user,
        depth=current_folder.depth+1,
        path__startswith=current_folder.path,
    )
    folders_list = []
    files_list = []
    if folders.exists():
        for f in folders:
            folders_list.append(f)
    if files.exists():
        for f in files:
            files_list.append(f)
    bread = []
    if current_folder.depth > 0:
        bread.append(current_folder)
        path = current_folder.path.split('/')
        depth = current_folder.depth
        while depth != 1:
            path.pop()
            depth -= 1
            folder = Folder.objects.filter(
                user=request.user,
                depth=depth,
                path='/'.join(path)
            ).first()
            bread.append(model_to_dict(folder))
    bread.append(top_dir)
    bread.reverse()
    bread = [i for i in enumerate(bread)]
    context['current_folder'] = current_folder
    context['folders'] = folders_list
    context['files'] = files_list
    context['bread'] = bread
    context['n_bread'] = len(bread)-1
    context['empty'] = (len(folders_list) == 0) and (len(files_list) == 0)
    return render(request, 'cloud/drive.html', context)


@login_required
def file_upload(request):
    r_id = 0
    try:
        if request.method == 'POST' and request.FILES['user-file']:
            f = request.FILES['user-file']
            folder_id = int(request.POST.get('folder-id'))
            folder = Folder.objects.filter(user=request.user, id=folder_id)
            if folder.exists():
                folder = folder.first()
                r_id = folder_id
                new_file = File.objects.create(
                    user=request.user,
                    folder=folder,
                    file=f
                )
                new_file.save()
                messages.success(
                    request, f"File [{os.path.basename(new_file.file.path)}] uploaded successfully!")
    except:
        folder_id = int(request.POST.get('folder-id'))
        folder = Folder.objects.filter(user=request.user, id=folder_id)
        if folder.exists():
            folder = folder.first()
            r_id = folder_id

    return redirect(f'/drive/?id={r_id}')


@login_required
def folder_create(request):
    r_id = 0
    try:
        if request.method == 'POST':
            folder_id = int(request.POST.get('folder-id'))
            folder_name = request.POST.get('folder-name')
            folder = Folder.objects.filter(user=request.user, id=folder_id)
            if folder.exists():
                folder = folder.first()
                r_id = folder_id
                if folder_name.strip() != '':
                    already = False
                    others = Folder.objects.filter(
                        user=request.user,
                        depth=folder.depth+1
                    )
                    for d in others:
                        if d.name == folder_name:
                            already = True
                            break
                    if not already:
                        new_folder = Folder.objects.create(
                            user=request.user,
                            name=folder_name,
                            depth=folder.depth+1,
                            path=f'{folder.path}/{int(time.time())}'
                        )
                        new_folder.save()
                        messages.success(
                            request, f"Folder [{folder_name}] created successfully!")
                    else:
                        messages.error(
                            request, f"Folder with name [{folder_name}] already exists!")
    except Exception as e:
        print(e)
        folder_id = int(request.POST.get('folder-id'))
        folder = Folder.objects.filter(user=request.user, id=folder_id)
        if folder.exists():
            folder = folder.first()
            r_id = folder_id

    return redirect(f'/drive/?id={r_id}')


@login_required
def file_delete(request):
    r_id = 0
    if request.method == 'GET':
        file_id = int(request.GET.get('file-id'))
        r_id = int(request.GET.get('folder-id'))
        f = File.objects.filter(user=request.user, id=file_id)
        if f.exists():
            f = f.first()
            name = os.path.basename(f.file.path)
            f.delete()
            messages.success(
                request, f"File [{name}] deleted successfully!")

    return redirect(f'/drive/?id={r_id}')


@login_required
def folder_delete(request):
    r_id = 0
    if request.method == 'GET':
        folder = int(request.GET.get('folder'))
        r_id = int(request.GET.get('folder-id'))
        folder = Folder.objects.filter(user=request.user, id=folder)
        if folder.exists():
            folder = folder.first()
            name = folder.name
            for d in Folder.objects.filter(user=request.user, path__startswith=folder.path):
                d.delete()
            folder.delete()
            messages.success(
                request, f"Folder [{name}] deleted successfully!")

    return redirect(f'/drive/?id={r_id}')


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
