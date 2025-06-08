from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _

from task_manager.statuses.models import Status
from task_manager.statuses.forms import StatusForm


class StatusesIndexView(ListView):
    model = Status
    context_object_name = 'statuses'
    template_name = 'statuses/index.html'


class StatusCreateView(CreateView):
    form_class = StatusForm
    template_name = 'statuses/form.html'
    success_url = reverse_lazy('statuses_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = False
        return context

    def form_valid(self, form):
        messages.success(self.request, _("Status successfully created"))
        return super().form_valid(form)


class StatusUpdateView(UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/form.html'
    success_url = reverse_lazy('statuses_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, _("Status successfully updated"))
        return super().form_valid(form)

class StatusDeleteView(DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses_index')
    context_object_name = 'status'

    def form_valid(self, form):
        messages.success(self.request, _("Status successfully deleted"))
        return super().form_valid(form)