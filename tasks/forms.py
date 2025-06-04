from django import forms
from .models import Task
from django.utils.translation import gettext_lazy as _
from task_manager.labels.models import Label
from task_manager.statuses.models import Status


class TaskForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label=_('Метки'),
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'tags']
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
            ),
        }
        labels = {
            'name': _('Имя'),
            'description': _('Описание'),
            'status': _('Статус'),
            'executor': _('Исполнитель'),
            'tags': _('Метки'),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Task.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(_("Задача с таким именем уже существует."))
        return name

    def save(self, commit=True):
        task = super().save(commit=commit)
        if commit:
            self.save_m2m()
        return task