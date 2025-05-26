from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .models import Task
from .forms import TaskForm


class TaskListView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to view tasks.')
            return redirect('login')
        task_list = Task.objects.all()
        return render(request, 'task_list.html', context={'task_list': task_list})


class TaskDetailView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to view task details.')
            return redirect('login')
        task = Task.objects.get(pk=kwargs.get('pk'))
        if not task:
            messages.error(request, 'Task not found')
            return redirect('task_list')
        return render(request, 'task_detail.html', context={'task': task})


class TaskCreateView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to create a task.')
            return redirect('login')
        form = TaskForm()
        return render(request, 'task_form.html', context={'form': form})
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to create a task.')
            return redirect('login')
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user.username
            task.save()
            form.save_m2m()
            messages.success(request, 'Task created successfully!')
            return redirect('task_list')  # Redirect to the task list after creation
        else:
            messages.error(request, 'There was an error creating the task. Please correct the errors below.')
            return render(request, 'task_form.html', context={'form': form})


class TaskUpdateView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to update a task.')
            return redirect('login')
        task = Task.objects.get(pk=kwargs.get('pk'))
        form = TaskForm(instance=task)

        return render(request, 'task_form.html', context={'form': form})
    
    def post(self, request, *args, **kwargs):
        # Here you would handle the form submission to update a task
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to update a task.')
            return redirect('login')
        form = TaskForm(request.POST, instance=Task.objects.get(pk=kwargs.get('pk')))
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_list')  # Redirect to the task list after update
        else:
            messages.error(request, 'There was an error updating the task. Please correct the errors below.')
            return render(request, 'task_form.html', context={'form': form})


class TaskDeleteView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to delete a task.')
            return redirect('login')
        # Here you would handle the deletion of a task
        task = Task.objects.get(pk=kwargs.get('pk'))
        if task.author != request.user.username:
            messages.error(request, 'You do not have permission to delete this task.')
            return redirect('task_list')  # добавить ошибку
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task_list')  # Redirect to the task list after deletion