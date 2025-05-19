from django.shortcuts import render, redirect
from django.views import View

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')

class UserUpdateView(View):
    def get(self, request, *args, **kwargs): #обновление данных пользователя
        return render(request, 'user_form.html')
    def post(self, request, *args, **kwargs): #обновление данных пользователя
        return redirect('user_list')


class UserDeleteView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'user_confirm_delete.html')
    def post(self, request, *args, **kwargs):
        return redirect('user_list')


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        return redirect('home')


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')
    def post(self, request, *args, **kwargs):
        return redirect('home')
