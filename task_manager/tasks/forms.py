from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Task


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Переопределяем отображение исполнителя
        self.fields['executor'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}".strip() or obj.username

    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "labels"]
        labels = {
            "name": _("Name"),
            "description": _("Description"),
            "status": _("Status"),
            "executor": _("Executor"),
            "labels": _("Labels"),
        }
