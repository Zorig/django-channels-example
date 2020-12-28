from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Chat(TimeStampModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, allow_unicode=True, blank=True)

    def save(self, *args, **kwargs):
        if self.name:
            self.slug = slugify(self.name.replace(" ", "_"), allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("chat:room", kwargs={"slug": self.slug})


class Message(TimeStampModel):
    text = models.TextField()
    chat = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.author} on {self.created_at}"
