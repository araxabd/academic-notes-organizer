from django.db import models
from django.conf import settings

from .storage import NoteFileStorage
from .validators import validate_mimetype

note_file_storage = NoteFileStorage()

class Note(models.Model):
    title = models.CharField(max_length=150)
    desc = models.TextField(blank=True)
    content = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name="notes")
    tags =  models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class NoteFile(models.Model):
    title = models.CharField(max_length=200)
    desc = models.TextField(blank=True, null=True)
    note = models.ForeignKey('Note', on_delete=models.CASCADE, related_name='files')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="uploaded_files")
    file = models.FileField(upload_to='notes_files/', storage=note_file_storage, max_length=500, validators=[validate_mimetype])
    size = models.IntegerField(default=0)
    uploaded = models.DateTimeField(auto_now_add=True)
