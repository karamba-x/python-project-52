from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django_filters.views import FilterView
from task_manager.tasks.filter import TaskFilter
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task


class TasksIndexView(FilterView):
    model = Task
    template_name = 'tasks/index.html'
    filterset_class = TaskFilter
    context_object_name = 'tasks'

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/form.html'
    success_url = reverse_lazy('tasks_index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, _("Task successfully created"))
        return super().form_valid(form)

class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'task'

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/form.html'
    success_url = reverse_lazy('tasks_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, _("Task successfully updated"))
        return super().form_valid(form)

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks_index')
    context_object_name = 'task'

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if task.author != request.user:
            messages.error(request, _('''A task can only be deleted by its author.'''))
            return redirect('tasks_index')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, _("Task successfully deleted"))
        return super().form_valid(form)