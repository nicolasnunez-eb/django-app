from django.db import models
from django.conf import settings


class Priority(models.Model):

    def __str__(self):
        return self.name

    name = models.CharField(max_length=20)


class Task(models.Model):

    def __str__(self):
        return self.name
    event = models.CharField(max_length=40, default='')
    name = models.CharField(max_length=20)
    done = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    priority = models.ForeignKey(Priority, on_delete=models.PROTECT)
    author = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.CASCADE
    )

    @property
    def complete(self):
        return 'Finished' if not self.done else 'Undo'

    @property
    def icon_complete(self):
        return 'glyphicon glyphicon-check' if not self.done else 'glyphicon glyphicon-remove-sign'

    @property
    def boton_type(self):
        return 'btn btn-success' if not self.done else 'btn btn-warning'
