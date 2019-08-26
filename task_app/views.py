from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .models import Task


class TaskList(ListView):
    model = Task


class TaskForm(CreateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('task-list')


class TaskUpdate(UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('task-list')
