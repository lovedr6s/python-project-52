from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django_filters.views import FilterView
from .filters import TaskFilter
from .models import Task
from .forms import TaskForm


class TaskListView(FilterView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'task_list'
    filterset_class = TaskFilter

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

class TaskDetailView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect('login')
        task = Task.objects.get(pk=kwargs.get('pk'))
        if not task:
            messages.error(request, 'Задача не найдена')
            return redirect('task_list')
        return render(request, 'task_detail.html', context={'task': task})


class TaskCreateView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect('login')
        form = TaskForm()
        return render(request, 'task_form.html', context={'form': form, 'action': 'Создать задачу', 'button_action': 'Создать'})
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect('login')
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            form.save_m2m()
            messages.success(request, 'Задача успешно создана')
            return redirect('task_list')  # Redirect to the task list after creation
        else:
            messages.error(request, 'There was an error creating the task. Please correct the errors below.')
            return render(request, 'task_form.html', context={'form': form, 'action': 'Создать задачу', 'button_action': 'Создать'})


class TaskUpdateView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect('login')
        task = Task.objects.get(pk=kwargs.get('pk'))
        form = TaskForm(instance=task)

        return render(request, 'task_form.html', context={'form': form, 'action': 'Изменение задачи', 'button_action': 'Изменить'})
    
    def post(self, request, *args, **kwargs):
        # Here you would handle the form submission to update a task
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect('login')
        form = TaskForm(request.POST, instance=Task.objects.get(pk=kwargs.get('pk')))
        if form.is_valid():
            form.save()
            form.save_m2m()
            messages.success(request, 'Задача успешно изменена')
            return redirect('task_list')  # Redirect to the task list after update
        else:
            messages.error(request, 'There was an error updating the task. Please correct the errors below.')
            return render(request, 'task_form.html', context={'form': form, 'action': '', 'button_action': 'Изменить'})


class TaskDeleteView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect('login')
        # Here you would handle the deletion of a task
        task = Task.objects.get(pk=kwargs.get('pk'))
        if task.author != request.user:
            messages.error(request, 'Задачу может удалить только ее автор')
            return redirect('task_list')  # добавить ошибку
        task.delete()
        messages.success(request, 'Задача успешно удалена')
        return redirect('task_list')  # Redirect to the task list after deletion