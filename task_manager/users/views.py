from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from .forms import UserForm
from django.contrib import messages
from task_manager.tasks.models import Task


# Create your views here.

class UserUpdateView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if str(request.user.id) != str(kwargs.get('pk')):
            messages.error(request, 'У вас нет прав для изменения другого пользователя.')
            return redirect('user_list')
        return render(request, 'user_form.html', context={'form': UserForm(instance=request.user), 'action': 'Изменить пользователя'})
    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пользователь успешно изменен')
            return redirect('user_list')
        return render(request, 'user_form.html', context={'form': form, 'action': 'Изменить пользователя'})


class UserListView(View):
    def get(self, request, *args, **kwargs):
        user_list = User.objects.all()
        return render(request, 'user_list.html',
                      context={'user_list': user_list})


class UserCreateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'user_form.html', context={'form': UserForm(), 'action': 'Создать пользователя'})
    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь успешно создан')
            return redirect('login')
        else:
            return render(request, 'user_form.html', context={'form': form, 'action': 'Создать пользователя'})


class UserDeleteView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect('login')
        user = User.objects.get(id=kwargs.get('pk'))
        if str(user) != str(request.user.username):
            messages.error(request, 'У вас нет прав для изменения другого пользователя.')
            return redirect('user_list')
        if Task.objects.filter(author=user).exists():
            messages.error(request, 'Невозможно удалить пользователя, потому что он используется')
            return redirect('user_list')
        user.delete()
        messages.success(request, 'Пользователь успешно удален')
        return redirect('user_list')
