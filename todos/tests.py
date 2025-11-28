from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Todo
from datetime import date

class TodoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.todo = Todo.objects.create(
            title='Test Todo',
            description='Test Description',
            user=self.user
        )

    def test_todo_string_representation(self):
        self.assertEqual(str(self.todo), 'Test Todo')

    def test_todo_defaults(self):
        self.assertFalse(self.todo.resolved)

class TodoAuthTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.list_url = reverse('todo_list')
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.list_url)
        self.assertRedirects(response, f'{self.login_url}?next={self.list_url}')

    def test_login_works(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_registration(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!' # UserCreationForm expects password2 for confirmation
        })
        # Check if user is created
        self.assertTrue(User.objects.filter(username='newuser').exists())

class TodoCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_login(self.user)
        self.create_url = reverse('todo_create')
        self.list_url = reverse('todo_list')

    def test_create_todo(self):
        response = self.client.post(self.create_url, {
            'title': 'New Todo',
            'description': 'New Description',
            'due_date': '2025-12-31'
        })
        self.assertEqual(Todo.objects.count(), 1)
        self.assertEqual(Todo.objects.first().title, 'New Todo')

    def test_update_todo(self):
        todo = Todo.objects.create(title='Old Title', user=self.user)
        update_url = reverse('todo_update', args=[todo.pk])
        response = self.client.post(update_url, {
            'title': 'New Title',
            'description': 'Updated Description',
            'due_date': '2025-12-31',
            'resolved': False
        })
        todo.refresh_from_db()
        self.assertEqual(todo.title, 'New Title')

    def test_delete_todo(self):
        todo = Todo.objects.create(title='To Delete', user=self.user)
        delete_url = reverse('todo_delete', args=[todo.pk])
        response = self.client.post(delete_url)
        self.assertEqual(Todo.objects.count(), 0)

    def test_resolve_todo(self):
        todo = Todo.objects.create(title='To Resolve', user=self.user)
        resolve_url = reverse('todo_resolve', args=[todo.pk])
        response = self.client.get(resolve_url) # resolve is a GET request in views.py currently
        todo.refresh_from_db()
        self.assertTrue(todo.resolved)

class TodoIsolationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        self.todo1 = Todo.objects.create(title='User 1 Todo', user=self.user1)
        self.todo2 = Todo.objects.create(title='User 2 Todo', user=self.user2)

    def test_user1_cannot_see_user2_todos(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('todo_list'))
        self.assertContains(response, 'User 1 Todo')
        self.assertNotContains(response, 'User 2 Todo')

    def test_user1_cannot_edit_user2_todo(self):
        self.client.force_login(self.user1)
        update_url = reverse('todo_update', args=[self.todo2.pk])
        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 404) # Should return 404 because of get_queryset filtering
