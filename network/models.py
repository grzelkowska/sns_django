from tokenize import blank_re
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    
    def __str__(self):
        return f"{self.username}"


class Post(models.Model):
    entry = models.TextField(max_length=512)
    created_date = models.DateTimeField(default=timezone.now)
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name="all_creators")
    image = models.ImageField(null=True, blank=True, upload_to="image/")

    def __str__(self):
        return f"{self.entry} by {self.creator}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} likes {self.post}"


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} is following {self.following}"        