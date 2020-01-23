from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):

    title = models.CharField(max_length=150)
    text = models.TextField()
    publication_time = models.DateTimeField(default=timezone.now(), blank=True)
    likes = models.IntegerField(default=0)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-publication_time"]

    def __str__(self):
        return self.title

