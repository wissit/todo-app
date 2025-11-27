from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Todo
from .forms import TodoForm

class RegisterView(CreateView):
    template_name = 'todos/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('todo_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)

class TodoList(LoginRequiredMixin, ListView):
    model = Todo
    context_object_name = 'todos'

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

class TodoCreate(LoginRequiredMixin, CreateView):
    model = Todo
    form_class = TodoForm
    success_url = reverse_lazy('todo_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TodoUpdate(LoginRequiredMixin, UpdateView):
    model = Todo
    form_class = TodoForm
    success_url = reverse_lazy('todo_list')

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

class TodoDelete(LoginRequiredMixin, DeleteView):
    model = Todo
    context_object_name = 'todo'
    success_url = reverse_lazy('todo_list')

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

@login_required
def resolve_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.resolved = not todo.resolved
    todo.save()
    return redirect('todo_list')
