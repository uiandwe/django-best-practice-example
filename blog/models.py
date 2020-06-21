from django.db import models
from django.conf import settings


class Post(models.Model):
    message = models.TextField(blank=True, help_text="메시지")
    public = models.BooleanField(default=False, help_text="공개 여부")
    count = models.IntegerField(default=0, help_text="읽은 유저 수")
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name="user",
    )
