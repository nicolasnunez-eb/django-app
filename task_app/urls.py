from django.conf.urls import url
from .views import TaskList
from .views import TaskForm
from .views import TaskUpdate

urlpatterns = [
    url(r'^$', TaskList.as_view(), name='task-list'),
    url(r'^create', TaskForm.as_view(), name='task-form'),
    url(r'update/(?P<pk>[0-9]+)/$', TaskUpdate.as_view(), name='task-update')
]
