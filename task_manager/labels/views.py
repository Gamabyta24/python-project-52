from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Label
from .forms import LabelForm


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = "labels/index.html"
    context_object_name = "labels"
    login_url = reverse_lazy("login")


class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = "labels/create.html"
    success_url = reverse_lazy("labels")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request, _("Label successfully created"))
        return super().form_valid(form)


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = "labels/update.html"
    success_url = reverse_lazy("labels")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request, _("Label successfully updated"))
        return super().form_valid(form)


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = "labels/delete.html"
    success_url = reverse_lazy("labels")
    login_url = reverse_lazy("login")

    def post(self, request, *args, **kwargs):
        label = self.get_object()
        # Проверяем, используется ли метка в задачах
        if label.tasks.exists():
            messages.error(self.request, _("Cannot delete a label that is in use"))
            return redirect("labels")
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, _("Label successfully deleted"))
        return super().form_valid(form)
