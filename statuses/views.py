from django.shortcuts import render, redirect
from django.views import View
from .models import Status
from .forms import StatusForm

class StatusListView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        statuses = Status.objects.all()
        return render(request, 'status_list.html', context={'statuses': statuses})


class StatusCreateView(View):
    def get(self, request, *args, **kwargs):
        form = StatusForm()
        return render(request, 'status_form.html', context={'form': form})
    def post(self, request, *args, **kwargs):
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('status_list')
        else:
            return render(request, 'status_form.html', context={'form': form})


class StatusUpdateView(View):
    def get(self, request, *args, **kwargs):
        form = StatusForm(instance=Status.objects.get(pk=kwargs['pk']))
        return render(request, 'status_form.html', context={'form': form})
    def post(self, request, *args, **kwargs):
        status = Status.objects.get(pk=kwargs['pk'])
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            return redirect('status_list')
        return redirect('status_list')


class StatusDeleteView(View):
    def post(self, request, *args, **kwargs):
        status = Status.objects.get(pk=kwargs['pk'])
        status.delete()
        return redirect('status_list')

