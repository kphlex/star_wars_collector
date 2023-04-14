from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from register.models import Profile

class People(models.Model):
    name = models.CharField(max_length=255)
    hair_color = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Starships(models.Model):
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Planets(models.Model):
    name = models.CharField(max_length=255)
    population = models.CharField(max_length=255)
    terrain = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)