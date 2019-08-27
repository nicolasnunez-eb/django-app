from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from .models import Task
from django.shortcuts import redirect


class TaskList(ListView):
    # model = Task
    def get_queryset(self):
        return Task.objects.filter(author=self.request.user)


class TaskForm(CreateView):
    model = Task
    fields = ['name', 'done', 'priority']
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save()
        return super().form_valid(form)


class TaskUpdate(UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('task-list')


class Logout(LogoutView):
    pass


def task_done(request, pk):
    task = Task.objects.get(pk=pk)
    task.done = not task.done
    task.save()
    return redirect('task-list')


def delete_task(request, pk):
    task = Task.objects.get(pk=pk)
    task.delete()
    return redirect('task-list')
