from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView

from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import HttpResponse
from eventbrite import Eventbrite
from .models import Task


class TaskList(ListView):
    # model = Task
    def get_context_data(self, **kwargs):
        context = context = super(TaskList, self).get_context_data(**kwargs)
        context['event'] = self.kwargs['pk_event']
        return context

    def get_queryset(self):
        return Task.objects.filter(event=self.kwargs['pk_event'])


class TaskForm(CreateView):
    model = Task
    fields = ['name', 'done', 'priority']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.event = self.kwargs['pk_event']
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('task-list', kwargs={'pk_event':self.kwargs['pk_event']})


class TaskUpdate(UpdateView):
    model = Task
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('task-list', kwargs={'pk_event':self.kwargs['pk_event']})


class Logout(LogoutView):
    pass


class EventsList(TemplateView):
    template_name = 'task_app/event-list.html'

    def get_context_data(self, **kwargs):
        context = super(EventsList, self).get_context_data(**kwargs)
        context['events'] = self.get_events(self.request.user.social_auth.all()[0])
        return context

    def get_events(self, user):
        eventbrite = Eventbrite(user.access_token)
        events = eventbrite.get('/users/me/events')['events']
        return events


class Event(TemplateView):
    template_name = 'task_app/event.html'

    def get_context_data(self, **kwargs):
        context = super(Event, self).get_context_data(**kwargs)
        context['event'] = self.get_event(self.kwargs['pk_event'])
        return context

    def get_event(self, event_id):
        eventbrite = Eventbrite(
            self.request.user.social_auth.all()[0].access_token
            )
        event = eventbrite.get_event(event_id)
        return event


def task_done(request, **kwargs):
    task = Task.objects.get(pk=kwargs['pk'])
    task.done = not task.done
    task.save()
    return redirect('task-list', pk_event=kwargs['pk_event'])


def delete_task(request, **kwargs):
    task = Task.objects.get(pk=kwargs['pk'])
    task.delete()
    return redirect('task-list', pk_event=kwargs['pk_event'])
