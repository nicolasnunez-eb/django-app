from django.conf.urls import url
from .views import TaskList, TaskForm, TaskUpdate
from .views import task_done, delete_task

urlpatterns = [
    url(r'^$', TaskList.as_view(), name='task-list'),
    url(r'^create', TaskForm.as_view(), name='task-form'),
    url(r'update/(?P<pk>[0-9]+)/$', TaskUpdate.as_view(), name='task-update'),
    url(r'done/(?P<pk>[0-9]+)/$', task_done, name='task-done'),
    url(r'delete/(?P<pk>[0-9]+)/$', delete_task, name='task-delete')
]
