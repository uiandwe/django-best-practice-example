from django.db import models


class Post(models.Model):
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
