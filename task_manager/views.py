from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.tasks.models import Task

from .forms import UserRegistrationForm
from .mixins import UserPermissionMixin


def index(request):
    return render(request, "index.html")


class UserListView(ListView):
    model = User
    template_name = "users/index.html"
    context_object_name = "users"


class UserCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request, _("User successfully registered"))
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UserPermissionMixin, UpdateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "users/update.html"
    success_url = reverse_lazy("users")

    def form_valid(self, form):
        messages.success(self.request, _("User successfully updated"))
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, UserPermissionMixin, DeleteView):
    model = User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users")

    def post(self, request, *args, **kwargs):
        user = self.get_object()

        if Task.objects.filter(Q(creator=user) | Q(executor=user)).exists():
            messages.error(
                self.request,
                _("Cannot delete user because they have associated tasks"),
            )
            return redirect("users")

        messages.success(self.request, _("User successfully deleted"))
        return super().post(request, *args, **kwargs)


class UserLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = "users/login.html"
    next_page = reverse_lazy("index")

    def form_valid(self, form):
        messages.success(self.request, _("You are logged in"))
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("index")

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _("You are logged out"))
        return super().dispatch(request, *args, **kwargs)
