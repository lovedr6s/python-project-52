from django import forms
from .models import Status

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Status.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Status with this name already exists.")
        return name

    def save(self, commit=True):
        status = super().save(commit=False)
        if commit:
            status.save()
        return status