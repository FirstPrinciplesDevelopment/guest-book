import uuid
from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.contrib import admin


class AvatarImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField()

    def __str__(self):
        return self.url


class Visitor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    avatar = models.ForeignKey(AvatarImage, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Visit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    visit_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.visit_datetime.isoformat()
