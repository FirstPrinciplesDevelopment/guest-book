from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.contrib import admin


class Visitor(models.Model):
    name = models.CharField(max_length=200)
    avatar_url = models.URLField()

    def __str__(self) -> str:
        return self.name


class Visit(models.Model):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    visit_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.visit_datetime.isoformat()


class AvatarImage(models.Model):
    url = models.URLField()

    def __str__(self):
        return self.url
