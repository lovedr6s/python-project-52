from django.shortcuts import render, redirect
from django.views import View
from .models import Task
from .forms import TaskForm


class TaskListView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        task_list = Task.objects.all()
        return render(request, 'task_list.html', context={'task_list': task_list})


class TaskDetailView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        task = Task.objects.get(pk=kwargs.get('pk'))
        if not task:
            return render(request, 'task_detail.html', context={'error': 'Task not found'})
        return render(request, 'task_detail.html', context={'task': task})


class TaskCreateView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        form = TaskForm()
        return render(request, 'task_form.html', context={'form': form})
    
    def post(self, request, *args, **kwargs):
        # Here you would handle the form submission to create a task
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user.username
            task.save()
            return redirect('task_list')  # Redirect to the task list after creation
        else:
            return render(request, 'task_form.html', context={'form': form})


class TaskUpdateView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        task = Task.objects.get(pk=kwargs.get('pk'))
        form = TaskForm(instance=task)

        return render(request, 'task_form.html', context={'form': form})
    
    def post(self, request, *args, **kwargs):
        # Here you would handle the form submission to update a task
        if not request.user.is_authenticated:
            return redirect('login')
        form = TaskForm(request.POST, instance=Task.objects.get(pk=kwargs.get('pk')))
        if form.is_valid():
            form.save()
            return redirect('task_list')  # Redirect to the task list after update
        else:
            return render(request, 'task_form.html', context={'form': form})


class TaskDeleteView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        # Here you would handle the deletion of a task
        task = Task.objects.get(pk=kwargs.get('pk'))
        if task.author != request.user.username:
            return redirect('task_list')  # добавить ошибку
        task.delete()
        return redirect('task_list')  # Redirect to the task list after deletion