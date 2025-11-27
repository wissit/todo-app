from django.urls import path
from .views import TodoList, TodoCreate, TodoUpdate, TodoDelete, resolve_todo, RegisterView

urlpatterns = [
    path('', TodoList.as_view(), name='todo_list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('create/', TodoCreate.as_view(), name='todo_create'),
    path('update/<int:pk>/', TodoUpdate.as_view(), name='todo_update'),
    path('delete/<int:pk>/', TodoDelete.as_view(), name='todo_delete'),
    path('resolve/<int:pk>/', resolve_todo, name='todo_resolve'),
]
