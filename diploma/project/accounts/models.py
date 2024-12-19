from django.db import models
from django.contrib.auth.models import User

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # пользователь, загрузивший файл
    file = models.FileField(upload_to='uploads/')  # путь к файлу
    uploaded_at = models.DateTimeField(auto_now_add=True)  # дата загрузки

    def __str__(self):
        return f"{self.user.username} - {self.file.name}"
