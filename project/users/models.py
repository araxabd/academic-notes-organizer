from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    #TODO: add marketplace features
    def __str__(self):
        return self.username
