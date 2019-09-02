from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView

from django.urls import reverse_lazy
from django.shortcuts import redirect
from eventbrite import Eventbrite
from .models import Task
from pure_pagination.mixins import PaginationMixin
from pure_pagination.paginator import Paginator, Page


class TaskList(PaginationMixin, ListView):
    # model = Task
    paginate_by = 5

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


class ApiQuerySet:
    def __init__(self, api_result):
        self.api_result = api_result
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.api_result['events']):
            raise StopIteration
        next_value = self.api_result['events'][self.index]
        self.index += 1
        return next_value

    def count(self):
        return self.api_result['pagination']['object_count']


class ApiPaginator(Paginator):
    def page(self, number):
        "Returns a Page object for the given 1-based page number."
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count
        return Page(self.object_list, number, self)


class EventsList(PaginationMixin, ListView):
    template_name = 'task_app/event-list.html'
    paginate_by = 5
    paginator_class = ApiPaginator

    def get_queryset(self):
        return ApiQuerySet(self.get_events(self.request.user.social_auth.all()[0]))

    def get_events(self, user):
        eventbrite = Eventbrite(user.access_token)
        page_number = self.request.GET['page'] if 'page' in self.request.GET else 1
        events = eventbrite.get(
            '/users/me/events?page_size={}&page={}'.format(
                self.paginate_by,
                page_number,
            )
        )
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
