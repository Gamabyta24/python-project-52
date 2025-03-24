from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import UserRegistrationForm
from django.db.models import Q
from task_manager.tasks.models import Task
from django.http import HttpResponse
# def index(request):
#     return render(request,'index.html')
def index(request):
    a = None
    a.hello() # Creating an error with an invalid line of code
    return HttpResponse("Hello, world. You're at the pollapp index.")

class UserListView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'

class UserCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        messages.success(self.request, _('User successfully registered'))
        return super().form_valid(form)

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserRegistrationForm 
    template_name = 'users/update.html'
    success_url = reverse_lazy('users')
    
    def test_func(self):
        # Проверка, что пользователь изменяет только свой профиль
        return self.request.user.id == self.kwargs['pk']
    
    def form_valid(self, form):
        messages.success(self.request, _('User successfully updated'))
        return super().form_valid(form)
    
    def handle_no_permission(self):
        messages.error(self.request, _('You have no rights to change another user'))
        return redirect('users')

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users')
    
    def test_func(self):
        # Проверка, что пользователь удаляет только свой профиль
        return self.request.user.id == self.kwargs['pk']
    
    # def form_valid(self, form):
    #     messages.success(self.request, _('User successfully deleted'))
    #     return super().form_valid(form)
    def post(self, request, *args, **kwargs):
        user = self.get_object()
        
        # Check if user is associated with any tasks
        if Task.objects.filter(Q(creator=user) | Q(executor=user)).exists():
            messages.error(self.request, _('Cannot delete user because they have associated tasks'))
            return redirect('users')
        
        messages.success(self.request, _('User successfully deleted'))
        return super().post(request, *args, **kwargs)
    
    def handle_no_permission(self):
        messages.error(self.request, _('You have no rights to delete another user'),extra_tags='danger')
        return redirect('users')

class UserLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    next_page = reverse_lazy('index')
    
    def form_valid(self, form):
        messages.success(self.request, _('You are logged in'))
        return super().form_valid(form)

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')
    
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)