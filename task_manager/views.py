from django.shortcuts import render, redirect
from django.views import View
from users.models import User
from users.forms import UserForm
from django.contrib.auth.hashers import make_password, check_password

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')

class UserUpdateView(View):
    def get(self, request, *args, **kwargs):
        if request.session.get('user_id') is None:
            return redirect('login')
        return render(request, 'user_form.html')
    def post(self, request, *args, **kwargs):
        return redirect('user_list')


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        if 'user_id' in request.session:
            del request.session['user_id']
        return redirect('home')


class UserListView(View):
    def get(self, request, *args, **kwargs):
        user_list = User.objects.all()
        return render(request, 'user_list.html', context={'user_list': user_list})


class UserCreateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'user_form.html', context={'form': UserForm()})
    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
        else:
            return render(request, 'user_form.html', context={'form': form})


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username, password=password).first()
        if user and check_password(password, user.password):
            request.session['user_id'] = user.id
            return redirect('home')
        else:
            return render(request, 'login.html', context={'error': 'Invalid login or password'})

class UserDeleteView(View):
    def post(self, request, *args, **kwargs):
        if request.session.get('user_id') is None:
            return redirect('login')
        user_id = kwargs.get('pk')
        user = User.objects.get(id=user_id)
        user.delete()
        return redirect('user_list')
