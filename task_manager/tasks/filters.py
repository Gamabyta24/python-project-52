import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Task
from task_manager.labels.models import Label
from django.contrib.auth.models import User
from task_manager.statuses.models import Status


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        label=_("Status"),
        queryset=Status.objects.all(),  # Use .all() as a method call
    )

    executor = django_filters.ModelChoiceFilter(
        label=_("Executor"),
        queryset=User.objects.all(),  # Use .all() as a method call
    )

    labels = django_filters.ModelChoiceFilter(
        label=_("Label"),
        queryset=Label.objects.all(),  # Use .all() as a method call
        method="filter_by_labels",
    )

    self_tasks = django_filters.BooleanFilter(
        label=_("Only my tasks"),
        method="filter_self_tasks",
        widget=forms.CheckboxInput,
    )

    def filter_by_labels(self, queryset, name, value):
        if value:
            return queryset.filter(labels=value)
        return queryset

    def filter_self_tasks(self, queryset, name, value):
        if value and hasattr(self, "request"):
            return queryset.filter(creator=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ["status", "executor", "labels", "self_tasks"]
