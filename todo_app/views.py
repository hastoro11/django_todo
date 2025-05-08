from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import LoginForm
from .models import TODO


class HomeView(LoginRequiredMixin, View):
    login_url = reverse_lazy('todo_app:login')

    def get(self, request):
        todos = TODO.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'todo_app/index.html', {
            'todos': todos
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
