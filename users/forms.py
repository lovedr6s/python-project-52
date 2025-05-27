from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        labels = {
            'username': 'Имя пользователя',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        help_texts = {
        'username': '',
        'first_name': '',
        'last_name': '',
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Пользователь с таким именем уже существует.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if not password1 or not password2:
            raise forms.ValidationError("Для подтверждения введите, пожалуйста, пароль ещё раз.")
        if password1 != password2:
            raise forms.ValidationError("Введенные пароли не совпадают.")
        if len(password1) < 8:
            raise forms.ValidationError("Ваш пароль должен содержать как минимум 8 символа.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user