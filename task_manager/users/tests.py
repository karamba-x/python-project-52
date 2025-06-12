from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User

class UserViewTests(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.user = User.objects.get(pk=1)  # bigsmoke
        self.other_user = User.objects.get(pk=2)  # cj

    def test_user_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('users_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_user_create_view(self):
        response = self.client.post(reverse('user_create'), {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'pass12345',
            'password2': 'pass12345'
        })
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_update_view_as_self(self):
        self.client.force_login(self.user)
        url = reverse('user_update', args=[self.user.id])
        response = self.client.post(url, {
            'username': 'updateduser',
            'first_name': 'Updated',
            'last_name': 'Name',
        })
        self.assertRedirects(response, reverse('users_index'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')

    def test_user_update_view_as_other(self):
        self.client.force_login(self.other_user)
        url = reverse('user_update', args=[self.user.id])
        response = self.client.post(url, {
            'username': 'hacker',
        })
        self.assertRedirects(response, reverse('users_index'))
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.username, 'hacker')

    def test_user_delete_view_as_self(self):
        self.client.force_login(self.user)
        url = reverse('user_delete', args=[self.user.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('users_index'))
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    def test_user_delete_view_as_other(self):
        self.client.force_login(self.other_user)
        url = reverse('user_delete', args=[self.user.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('users_index'))
        self.assertTrue(User.objects.filter(id=self.user.id).exists())