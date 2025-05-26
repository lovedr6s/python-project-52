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
            messages.error(request, 'You must be logged in to view labels.')
            return redirect('login')
        labels = Label.objects.all()
        return render(request, 'label_list.html', context={'labels': labels})


class LabelCreateView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to create a label.')
            return redirect('login')
        form = LabelForm()
        return render(request, 'label_form.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to create a label.')
            return redirect('login')
        form = LabelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Label created successfully!')
            return redirect('label_list')
        else:
            messages.error(request, 'There was an error creating the label. Please correct the errors below.')
            return request(request, 'label_form.html', context={'form': form})


class LabelUpdateView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to update a label.')
            return redirect('login')
        form = LabelForm(instance=Label.objects.get(pk=kwargs.get('pk')))
        if not form:
            messages.error(request, 'Label not found')
            return redirect('label_list')
        
        return render(request, 'label_form.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to update a label.')
            return redirect('login')
        form = LabelForm(request.POST, instance=Label.objects.get(pk=kwargs.get('pk')))
        if form.is_valid():
            form.save()
            messages.success(request, 'Label updated successfully!')
            return redirect('label_list')
        else:
            messages.error(request, 'There was an error updating the label. Please correct the errors below.')
            return render(request, 'label_form.html', context={'form': form})


class LabelDeleteView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to delete a label.')
            return redirect('login')
        #получить все теги из tasks и если есть теги с этим label, то не удалять
        if Label.objects.get(pk=kwargs.get('pk')).tasks.exists():
            messages.error(request, 'Cannot delete label with associated tasks.')
            return redirect('label_list')
        label = Label.objects.get(pk=kwargs.get('pk'))
        label.delete()
        messages.success(request, 'Label deleted successfully!')
        return redirect('label_list')