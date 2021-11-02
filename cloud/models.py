import os
import shutil
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

from private_storage.fields import PrivateFileField
# Create your models here.


def file_path(self, filename):
    path = 'user_files'
    path = os.path.join(path, self.folder.path)
    path = os.path.join(path, filename)
    return path


def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


class Folder(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    depth = models.IntegerField(default=0)
    name = models.CharField(
        max_length=500,
        default='New Folder'
    )
    path = models.CharField(
        max_length=500,
        default='0'
    )

    def delete(self, *args, **kwargs):
        path = os.path.join(
            settings.PRIVATE_STORAGE_ROOT,
            'user_files',
            self.path
        )
        if os.path.isdir(path):
            shutil.rmtree(path)

        super(Folder, self).delete(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.user.pk}_{self.name}'

    def __repr__(self) -> str:
        return self.__str__()


class File(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    file = PrivateFileField(
        upload_to=file_path,
        verbose_name="Upload File",
    )

    def filename(self):
        return os.path.basename(self.file.name)

    def get_prop(self):
        path = os.path.join(
            settings.PRIVATE_STORAGE_ROOT,
            self.file.name
        )
        data = {}
        data["name"] = self.filename()
        data["size"] = sizeof_fmt(self.file.size)
        data["info"] = os.popen(f'file -b "{path}"').read().strip()
        data["date"] = self.date.strftime("%m/%d/%Y")
        return data

    def rename(self, name):
        new_file = os.path.join(
            os.path.dirname(self.file.name),
            name)
        new_path = os.path.join(settings.PRIVATE_STORAGE_ROOT, new_file)
        if not os.path.isfile(new_path):
            os.rename(
                os.path.join(
                    settings.PRIVATE_STORAGE_ROOT,
                    self.file.name
                ),
                new_path)
            self.file.name = new_file
            self.save()
            return True
        return False

    def delete(self, *args, **kwargs):
        if os.path.isfile(self.file.path):
            os.remove(self.file.path)

        super(File, self).delete(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.user.pk}_{self.file.name}'

    def __repr__(self) -> str:
        return self.__str__()


class ShareFile(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(
        User,
        related_name='file_owner',
        on_delete=models.CASCADE
    )
    viewer = models.ForeignKey(
        User,
        related_name='file_viewer',
        on_delete=models.CASCADE
    )
    file = models.ForeignKey(File, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.owner.pk}_{self.viewer.pk}_{self.file.filename()}'

    def __repr__(self) -> str:
        return self.__str__()
