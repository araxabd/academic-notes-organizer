from django.db import models
from django.conf import settings
from .validators import validate_score

class Rating(models.Model):
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ratings")
    score = models.PositiveSmallIntegerField(validators=[validate_score])

    def __str__(self):
        return f"{self.user.username} > {self.course.title} : {self.score}"

class Comment(models.Model):
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} > {self.course.title}"
