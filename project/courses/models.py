from django.db import models
from django.conf import settings

class Course(models.Model):
    title = models.CharField(max_length=150)
    desc = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses')

    is_public = models.BooleanField(default=False)
    price = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.title
