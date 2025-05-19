from django.shortcuts import render
from django.views import View
from .models import User
from django.shortcuts import redirect
# Create your views here.

class UserListView(View):
    def get(self, request, *args, **kwargs):
        user_list = User.objects.all()
        return render(request, 'user_list.html', context={'user_list': user_list})


class UserCreateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'user_form.html')
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user = User(username=username, password=password, first_name=first_name, last_name=last_name)
        user.save()
        return redirect('user_list')