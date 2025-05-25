from django.shortcuts import render, redirect
from django.views import View
from users.forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')


class UserUpdateView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return render(request, 'user_form.html', context={'form': UserForm(instance=request.user)})
    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('user_list')
        return render(request, 'user_form.html', context={'form': form})


class UserListView(View):
    def get(self, request, *args, **kwargs):
        user_list = User.objects.all()
        return render(request, 'user_list.html',
                      context={'user_list': user_list})


class UserCreateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'user_form.html', context={'form': UserForm()})
    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, 'user_form.html', context={'form': form})


class UserDeleteView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        user_id = kwargs.get('pk')
        user = User.objects.get(id=user_id)
        user.delete()
        return redirect('user_list')
