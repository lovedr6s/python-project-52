from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']
    def clean_username(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if not password or not confirm_password:
            raise forms.ValidationError("Оба поля пароля обязательны.")
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return cleaned_data