from django import forms
from django.utils.translation import gettext_lazy as _

from task_manager.tasks.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']

        labels = {
            'name': _('Name'),
            'description': _('Description'),
            'status': _('Status'),
            'executor': _('Executor'),
            'labels': _('Labels')
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': _('Name'),
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'placeholder': _('Description'),
                'class': 'form-control',
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
            }),
            'executor': forms.Select(attrs={
                'class': 'form-control',
            }),
            'labels': forms.SelectMultiple(attrs={
                'class': 'form-control',
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['executor'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"