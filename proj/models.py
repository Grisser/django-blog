from django.db import models


class Post(models.Model):

    title = models.CharField(max_length=150)
    text = models.TextField()
    publication_time = models.DateTimeField()
    author = models.IntegerField()

    class Meta:
        ordering = ["-publication_time"]

    def __str__(self):
        return self.title

