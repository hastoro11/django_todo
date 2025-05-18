from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import LoginForm, TODOForm
from .models import TODO


class HomeView(LoginRequiredMixin, View):
    login_url = reverse_lazy('todo_app:login')

    def get(self, request):
        todo_form = TODOForm()
        todos = TODO.objects.filter(user=request.user).order_by('archived', 'completed', 'created_at')

        return render(request, 'todo_app/index.html', {
            'todos': todos,
            'todo_form': todo_form,
        })


class EditTodoView(LoginRequiredMixin, View):
    login_url = reverse_lazy('todo_app:login')

    def get(self, request, pk):
        instance = TODO.objects.get(pk=pk)
        if not isinstance(instance, TODO):
            return redirect('todo_app:home')
        todo_form = TODOForm(initial={'title': instance.title})
        return render(request, 'todo_app/edit_todo.html', {
            'todo_form': todo_form,
            'todo': instance,
        })

    def post(self, request, pk):
        print('🎈')
        instance = TODO.objects.get(pk=pk)
        todo_form = TODOForm(request.POST)
        if todo_form.is_valid():
            title = todo_form.cleaned_data['title']
            print('⏰', instance.title, instance.created_at)
            instance.title = title
            instance.save()
            return redirect('todo_app:home')
        else:
            return render(request, 'todo_app/edit_todo.html', {
                'todo_form': todo_form,
                'todo': instance,
            })


# TODO: custom clean

def delete_todo(request, pk):
    instance = TODO.objects.get(pk=pk)
    instance.archived = not instance.archived
    instance.save()
    return redirect('todo_app:home')


def complete_todo(request, pk):
    instance = TODO.objects.get(pk=pk)
    instance.completed = not instance.completed
    instance.save()
    return redirect('todo_app:home')

def add_todo(request):
    if request.method == 'POST':
        todo_form = TODOForm(request.POST)
        if todo_form.is_valid():
            title = todo_form.cleaned_data.get('title')
            todo = TODO(title=title, user=request.user)
            todo.save()
            return redirect('todo_app:home')
        else:
            todos = TODO.objects.filter(user=request.user).order_by('-created_at')
            return render(request, 'todo_app/index.html', {
                'todos': todos,
                'todo_form': todo_form
            })


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'todo_app/login.html', {
            'form': form
        })

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('todo_app:login_complete')
            else:
                messages.error(request, 'Username/password don\'t match')
                return render(request, 'todo_app/login.html', {
                    'form': form
                })
        else:
            return render(request, 'todo_app/login.html', {
                'form': form
            })


def login_complete(request):
    if not request.user.is_authenticated:
        return redirect('todo_app:login')
    return render(request, 'todo_app/login_complete.html')


def log_out(request):
    logout(request)
    return redirect('todo_app:login')
