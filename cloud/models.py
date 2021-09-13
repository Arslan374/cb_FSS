import os
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


def file_path(self, filename):
    path = 'user_files'
    path = os.path.join(path, self.folder.path)
    path = os.path.join(path, str(self.folder.pk))
    path = os.path.join(path, filename)
    return path


class Folder(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    name = models.CharField(
        max_length=500,
        default='New Folder'
    )
    path = models.CharField(
        max_length=500,
        default='.'
    )

    def __str__(self) -> str:
        return f'{self.user.pk}_{self.name}'

    def __repr__(self) -> str:
        return self.__str__()


class File(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    file = models.FileField(
        default='.tmp',
        upload_to=file_path,
        verbose_name="Upload File",
    )

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
        return f'{self.owner.pk}_{self.viewer.pk}_{self.file.name}'

    def __repr__(self) -> str:
        return self.__str__()
