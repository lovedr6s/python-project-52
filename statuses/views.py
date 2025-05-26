from django.shortcuts import render, redirect
from django.views import View
from .models import Status
from .forms import StatusForm
from django.contrib import messages


class StatusListView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to view statuses.')
            return redirect('login')
        statuses = Status.objects.all()
        return render(request, 'status_list.html', context={'statuses': statuses})


class StatusCreateView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to create a status.')
            return redirect('login')
        form = StatusForm()
        return render(request, 'status_form.html', context={'form': form})
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to create a status.')
            return redirect('login')
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Status created successfully!')
            return redirect('status_list')
        else:
            messages.error(request, 'There was an error creating the status. Please correct the errors below.')
            return render(request, 'status_form.html', context={'form': form})


class StatusUpdateView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to update a status.')
            return redirect('login')
        form = StatusForm(instance=Status.objects.get(pk=kwargs['pk']))
        return render(request, 'status_form.html', context={'form': form})
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to update a status.')
            return redirect('login')
        status = Status.objects.get(pk=kwargs['pk'])
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(request, 'Status updated successfully!')
            return redirect('status_list')
        else:
            messages.error(request, 'There was an error updating the status. Please correct the errors below.')
            return render(request, 'status_form.html', context={'form': form})


class StatusDeleteView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
                    messages.error(request, 'You must be logged in to delete a status.')
                    return redirect('login')
        status = Status.objects.get(pk=kwargs['pk'])
        status.delete()
        messages.success(request, 'Status deleted successfully!')
        return redirect('status_list')

