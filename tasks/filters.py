import django_filters as filters
from django import forms
from tasks.models import Task
from statuses.models import Status
from labels.models import Label
from django.contrib.auth.models import User

class TaskFilter(filters.FilterSet):
    status = filters.ModelChoiceFilter(queryset=Status.objects.all())
    assignee = filters.ModelChoiceFilter(queryset=User.objects.all())
    labels = filters.ModelChoiceFilter(queryset=Label.objects.all(), field_name='tags')
    my_tasks_only = filters.BooleanFilter(
        label='Only my tasks',
        widget=forms.CheckboxInput,  # ВАЖНО! Здесь именно CheckboxInput, не BooleanWidget
        method='filter_my_tasks',
    )
    class Meta:
        model = Task
        fields = ['status', 'assignee', 'labels', 'my_tasks_only']
    def filter_my_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
