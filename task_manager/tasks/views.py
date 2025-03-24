from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from .models import Task
from .forms import TaskForm
from .filters import TaskFilter

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    login_url = reverse_lazy('login')
    filterset_class = TaskFilter
    def get_filterset(self, filterset_class):
        # Передаем request в фильтр для доступа к текущему пользователю
        filterset = super().get_filterset(filterset_class)
        filterset.request = self.request
        return filterset

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks')
    login_url = reverse_lazy('login')
    
    def form_valid(self, form):
        form.instance.creator = self.request.user
        messages.success(self.request, _('Task successfully created'))
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks')
    login_url = reverse_lazy('login')
    
    def form_valid(self, form):
        messages.success(self.request, _('Task successfully updated'))
        return super().form_valid(form)

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks')
    login_url = reverse_lazy('login')
    
    def test_func(self):
        # Only the creator can delete the task
        return self.get_object().creator == self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, _('Task successfully deleted'))
        return super().form_valid(form)
    
    def handle_no_permission(self):
        messages.error(self.request, _('Only the author of the task can delete it'))
        return redirect('tasks')

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'task'
    login_url = reverse_lazy('login')