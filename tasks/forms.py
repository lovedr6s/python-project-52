from django import forms
from .models import Task
from labels.models import Label  # Предполагается, что модель Status находится в приложении statuses
#удалить после создания модели Task и получать из statuses.models
class TaskForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # или forms.SelectMultiple для выпадающего списка
        required=False
    )
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'assignee', 'tags']
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Task.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Task with this name already exists.")
        return name
    def save(self, commit=True):
        task = super().save(commit=False)
        if commit:
            task.save()
            self.save_m2m()
        return task