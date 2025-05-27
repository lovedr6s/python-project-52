from django import forms
from .models import Task
from labels.models import Label


class TaskForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Метки',
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'assignee', 'tags']
        labels = {
            'name': 'Имя',
            'description': 'Описание',
            'status': 'Статус',
            'assignee': 'Исполнитель',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            widget = field.widget

            if isinstance(widget, forms.CheckboxSelectMultiple):
                # Bootstrap для чекбоксов можно добавить тут при желании
                widget.attrs.update({'class': 'form-check-input'})
            elif isinstance(widget, forms.Select):
                widget.attrs.update({'class': 'form-select'})
            else:
                widget.attrs.update({'class': 'form-control'})

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Task.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Задача с таким именем уже существует.")
        return name

    def save(self, commit=True):
        task = super().save(commit=False)
        if commit:
            task.save()
            self.save_m2m()
        return task