import django_filters as filters
from django import forms
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.contrib.auth.models import User

class TaskFilter(filters.FilterSet):
    status = filters.ModelChoiceFilter(queryset=Status.objects.all(), label='Статус')
    assignee = filters.ModelChoiceFilter(queryset=User.objects.all(), label='Исполнитель')
    labels = filters.ModelChoiceFilter(queryset=Label.objects.all(), field_name='tags', label='Метка')
    my_tasks_only = filters.BooleanFilter(
        label='Только свои задачи',
        widget=forms.CheckboxInput,
        method='filter_my_tasks',
    )
    class Meta:
        model = Task
        fields = ['status', 'assignee', 'labels', 'my_tasks_only']

    def filter_my_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
