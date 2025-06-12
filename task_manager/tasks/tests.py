from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status

from .models import Task

User = get_user_model()


class TaskTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.user = User.objects.first()
        self.status = Status.objects.first()
        self.label = Label.objects.first()
        self.client.force_login(self.user)

    def test_create_task(self):
        response = self.client.post(reverse('task_create'), {
            'name': 'Test Task',
            'description': 'Task description',
            'status': self.status.pk,
            'executor': self.user.pk,
            'labels': [self.label.pk],
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name='Test Task').exists())

    def test_update_task(self):
        task = Task.objects.first()
        response = self.client.post(reverse('task_update',
                                            kwargs={'pk': task.pk}), {
                                        'name': 'Updated Task',
                                        'description': 'Description',
                                        'status': self.status.pk,
                                        'executor': self.user.pk,
                                        'labels': [self.label.pk],
                                    })

        self.assertEqual(response.status_code, 302)
        task.refresh_from_db()
        self.assertEqual(task.name, 'Updated Task')