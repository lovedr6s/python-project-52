from django import forms
from .models import Task
from django.utils.translation import gettext_lazy as _
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from django.contrib.auth.models import User


class TaskForm(forms.ModelForm):
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Метки',
    )
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        label='Исполнитель'
    )
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('Имя'),
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('Описание'),
                }
            ),
            'status': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'executor': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            )
        }
        labels = {
            'name': 'Имя',
            'description': 'Описание',
            'status': 'Статус',
            'executor': 'Исполнитель',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['executor'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"
        self.fields['status'].queryset = Status.objects.all()