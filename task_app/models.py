from django.db import models
from django.conf import settings


class Priority(models.Model):

    def __str__(self):
        return self.name

    name = models.CharField(max_length=20)


class Task(models.Model):

    def __str__(self):
        return self.name

    name = models.CharField(max_length=20)
    done = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    priority = models.ForeignKey(Priority, on_delete=models.PROTECT)
    author = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.CASCADE
    )
