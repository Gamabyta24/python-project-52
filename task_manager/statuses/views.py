from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Status
from .forms import StatusForm


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = "statuses/index.html"
    context_object_name = "statuses"
    login_url = reverse_lazy("login")


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/create.html"
    success_url = reverse_lazy("statuses")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request, _("Status successfully created"))
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/update.html"
    success_url = reverse_lazy("statuses")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request, _("Status successfully updated"))
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = "statuses/delete.html"
    success_url = reverse_lazy("statuses")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        # We'll check for related tasks when we create the Task model
        # For now, we'll just add a success message
        messages.success(self.request, _("Status successfully deleted"))
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        status = self.get_object()
        if status.task_set.exists():
            messages.error(
                self.request, _("Невозможно удалить статус, потому что он используется")
            )
            return redirect("statuses")
        return super().post(request, *args, **kwargs)
