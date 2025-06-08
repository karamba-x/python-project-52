from django.test import TestCase
from django.urls import reverse
from task_manager.statuses.models import Status

class StatusesTests(TestCase):
    fixtures = ['users_fixture.json', 'statuses_fixture.json']

    def setUp(self):
        from django.contrib.auth.models import User
        self.user = User.objects.get(pk=1)  # или по username
        self.client.force_login(self.user)

    def test_status_list_view(self):
        url = reverse('statuses_index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/index.html')
        self.assertIn('statuses', response.context)
        self.assertTrue(len(response.context['statuses']) > 0)

    def test_status_create_view_get(self):
        url = reverse('status_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/form.html')

    def test_status_create_view_post(self):
        url = reverse('status_create')
        data = {'name': 'New Status'}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('statuses_index'))
        self.assertTrue(Status.objects.filter(name='New Status').exists())

    def test_status_update_view_get(self):
        status = Status.objects.first()
        url = reverse('status_update', args=[status.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/form.html')
        self.assertContains(response, status.name)

    def test_status_update_view_post(self):
        status = Status.objects.first()
        url = reverse('status_update', args=[status.pk])
        data = {'name': 'Updated Status'}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('statuses_index'))
        status.refresh_from_db()
        self.assertEqual(status.name, 'Updated Status')

    def test_status_delete_view_get(self):
        status = Status.objects.first()
        url = reverse('status_delete', args=[status.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/delete.html')

    def test_status_delete_view_post(self):
        status = Status.objects.first()
        url = reverse('status_delete', args=[status.pk])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('statuses_index'))
        self.assertFalse(Status.objects.filter(pk=status.pk).exists())