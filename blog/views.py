from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User

@login_required
def start(request):
   return redirect('profile') 

class ApplicationListView(ListView, LoginRequiredMixin):
    model = Application
    template_name = 'blog/active.html'
    context_object_name = 'applications'
    ordering = ['-date_applied']

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ApplicationListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Application.objects.filter(author=self.request.user, done=False)


class ApplicationDetailView(LoginRequiredMixin, DetailView):
    model = Application


class ApplicationCreateView(LoginRequiredMixin, CreateView):
    model = Application
    fields = ['title', 'content', 'receiver1', 'receiver2', 'attached_file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        print("Successful")
        permission = Permission()
        permission.phase = 1
        permission.parent = self.object
        permission.receiver = User.objects.filter(email=self.object.receiver1).first()
        permission.save()
        self.object.status = "Pending to " + str(permission.receiver.first_name) + " " + str(permission.receiver.last_name) + "\n"
        self.object.save()
        return reverse('active-list')

class PermissionListView(ListView, LoginRequiredMixin):
    model = Permission
    template_name = 'blog/pending.html'
    context_object_name = 'permissions'
    ordering = ['-date_applied']

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PermissionListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Permission.objects.filter(receiver=self.request.user, done=False)


class PermissionDetailView(LoginRequiredMixin, DetailView):
    model = Permission


def about(request):
    context = {
        'title': 'About ugh..'
    }
    return render(request, 'blog/about.html', context)

@login_required
def reject(request, pk):
    permission = Permission.objects.get(pk=pk)
    if request.user == permission.receiver:
        permission.parent.done=True
        permission.done=True
        permission.parent.status='Rejected by ' + permission.receiver.first_name + ' ' + permission.receiver.last_name
        permission.status = 'Rejected'
        permission.save()
        permission.parent.save()
    
    return redirect('pending-list')

def accept(request, pk):
    permission = Permission.objects.filter(id=pk).first()
    if request.user == permission.receiver:
        if permission.phase == 3:
            permission.parent.done=True
            permission.done=True
            permission.status = 'Accepted'
            permission.parent.status = "ACCEPTED"
            permission.parent.save()
            permission.save()
        elif permission.phase == 2:
            permission.done = True
            permission.status = 'Accepted'
            permission.parent.status = "Pending to Office"
            permission.parent.save()
            permission.save()
            permissionO = Permission()
            permissionO.receiver = User.objects.filter(username='office').first()
            permissionO.parent = permission.parent
            permissionO.phase = 3
            permissionO.save()
        else:
            permission.done = True
            permission.status = 'Accepted'
            permission.parent.status = "Pending to "+str(User.objects.filter(email = permission.parent.receiver2).first().first_name)+' '+str(User.objects.filter(email = permission.parent.receiver2).first().last_name)
            permission.parent.save()
            permission.save()
            permissionO = Permission()
            permissionO.receiver = User.objects.filter(email = permission.parent.receiver2).first()
            permissionO.parent = permission.parent
            permissionO.phase = 2
            permissionO.save()
    return redirect('pending-list')

class ApplicationHistoryListView(ListView, LoginRequiredMixin):
    model = Application
    template_name = 'blog/active.html'
    context_object_name = 'applications'
    ordering = ['-date_applied']

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ApplicationHistoryListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Application.objects.filter(author=self.request.user, done=True)

class PermissionHistoryListView(ListView, LoginRequiredMixin):
    model = Permission
    template_name = 'blog/pending.html'
    context_object_name = 'permissions'
    ordering = ['-date_applied']

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PermissionHistoryListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Permission.objects.filter(receiver=self.request.user, done=True)


