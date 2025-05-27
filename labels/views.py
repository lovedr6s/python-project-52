from django.shortcuts import render, redirect
from django.views import View
from .models import Label 
from .forms import LabelForm
from tasks.models import Task
from django.contrib import messages 
# Create your views here.
# МЕТКИ МОЖНО СОЗДАВАТЬ ТОЛЬКО ТУТ!!! В TASKS ЗАПРЕТИТЬ ВПИСЫВАТЬ И ДАТЬ ТОЛЬКО ВЫБИРАТЬ ИЗ ДОБАВЛЕННЫХ ТУТ

class LabelViews(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect('login')
        labels = Label.objects.all()
        return render(request, 'label_list.html', context={'labels': labels})


class LabelCreateView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect('login')
        form = LabelForm()
        return render(request, 'label_form.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect('login')
        form = LabelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Метка успешно создана')
            return redirect('label_list')
        else:
            messages.error(request, 'There was an error creating the label. Please correct the errors below.')
            return request(request, 'label_form.html', context={'form': form})


class LabelUpdateView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect('login')
        form = LabelForm(instance=Label.objects.get(pk=kwargs.get('pk')))
        if not form:
            messages.error(request, 'Метка не найдена')
            return redirect('label_list')
        
        return render(request, 'label_form.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect('login')
        form = LabelForm(request.POST, instance=Label.objects.get(pk=kwargs.get('pk')))
        if form.is_valid():
            form.save()
            messages.success(request, 'Метка успешно изменена')
            return redirect('label_list')
        else:
            messages.error(request, 'There was an error updating the label. Please correct the errors below.')
            return render(request, 'label_form.html', context={'form': form})


class LabelDeleteView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect('login')
        #получить все теги из tasks и если есть теги с этим label, то не удалять
        if Label.objects.get(pk=kwargs.get('pk')).tasks.exists():
            messages.error(request, 'Невозможно удалить метку, потому что она используется')
            return redirect('label_list')
        label = Label.objects.get(pk=kwargs.get('pk'))
        label.delete()
        messages.success(request, 'Метка успешно удалена')
        return redirect('label_list')