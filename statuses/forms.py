from django import forms
from .models import Status

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        labels = {
            'name': 'Имя',
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Status.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Cтатус с таким именем уже существует.")
        return name

    def save(self, commit=True):
        status = super().save(commit=False)
        if commit:
            status.save()
        return status