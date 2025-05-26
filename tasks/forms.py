from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'creator', 'tags']
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Task.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Task with this name already exists.")
        return name
    def save(self, commit=True):
        task = super().save(commit=False)
        if commit:
            task.save()
        return task