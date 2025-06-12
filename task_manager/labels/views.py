from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label


class LabelsIndexView(ListView):
    model = Label
    context_object_name = 'labels'
    template_name = 'labels/index.html'


class LabelCreateView(CreateView):
    form_class = LabelForm
    template_name = 'labels/form.html'
    success_url = reverse_lazy('labels_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = False
        return context

    def form_valid(self, form):
        messages.success(self.request, _("Label successfully created"))
        return super().form_valid(form)


class LabelUpdateView(UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/form.html'
    success_url = reverse_lazy('labels_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, _("Label successfully updated"))
        return super().form_valid(form)

class LabelDeleteView(DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels_index')
    context_object_name = 'label'

    def form_valid(self, form):
        label = self.get_object()
        if label.tasks.exists():
            messages.error(self.request, _("Cannot delete label because it is in use"))
            return redirect(self.success_url)
        messages.success(self.request, _("Label successfully deleted"))
        return super().form_valid(form)