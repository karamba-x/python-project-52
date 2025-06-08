from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from task_manager.users.forms import CustomUserCreateForm, CustomUserUpdateForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

class UserIndexView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'users/index.html'

class UserCreateView(CreateView):
    form_class = CustomUserCreateForm
    template_name = 'users/form.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, _("User successfully registrated"))
        return super().form_valid(form)

class UserUpdateView(UpdateView):
    model = User
    form_class = CustomUserUpdateForm
    template_name = 'users/form.html'
    success_url = reverse_lazy('users_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context

    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if user != request.user:
            messages.error(request, _('''You do not have permission 
                                         to modify another user.'''))
            return redirect('users_index')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, _('User successfully changed'))
        return super().form_valid(form)

class UserDeleteView(DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users_index')
    context_object_name = 'user'

    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if user != request.user:
            messages.error(request, _('''You do not have permission 
                                         to modify another user.'''))
            return redirect('users_index')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
    #     user = self.get_object()
    #     if user.tasks_created.exists():
    #         messages.error(self.request, _('''Cannot delete user
    #                                        because it is in use'''))
    #         return redirect(self.success_url)
        messages.success(self.request, _('User successfully deleted'))
        return super().form_valid(form)