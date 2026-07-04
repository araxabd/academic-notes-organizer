from django.db import models
from django.conf import settings

class Note(models.Model):
    title = models.CharField(max_length=150)
    desc = models.TextField(blank=True)
    content = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name="notes")
    tags =  models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    #TODO: add file attachment
    #TODO: add marketplace features

    def __str__(self):
        return self.title
