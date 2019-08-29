from django.conf.urls import url
from .views import TaskList, TaskForm, TaskUpdate, LogoutView, EventsList, Event
from .views import task_done, delete_task

urlpatterns = [
    url(r'^$', EventsList.as_view(), name='event-list'),
    url(r'^(?P<pk_event>[0-9]+)$', Event.as_view(), name='event'),
    url(r'^(?P<pk_event>[0-9]+)/tasks$', TaskList.as_view(), name='task-list'),
    url(r'^(?P<pk_event>[0-9]+)/tasks/create/$', TaskForm.as_view(), name='task-form'),
    url(r'^(?P<pk_event>[0-9]+)/tasks/update/(?P<pk>[0-9]+)$', TaskUpdate.as_view(), name='task-update'),
    url(r'^(?P<pk_event>[0-9]+)/tasks/done/(?P<pk>[0-9]+)$', task_done, name='task-done'),
    url(r'^(?P<pk_event>[0-9]+)/tasks/delete/(?P<pk>[0-9]+)$', delete_task, name='task-delete'),
    url(r'^logout', LogoutView.as_view(), name='logout')
]
