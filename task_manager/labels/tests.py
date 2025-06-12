from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Label

User = get_user_model()


class LabelTest(TestCase):
    fixtures = ['users.json', 'labels.json']

    def setUp(self):
        self.user = User.objects.first()
        self.label = Label.objects.first()
        self.client.force_login(self.user)

    def test_create_label(self):
        response = self.client.post(reverse('label_create'), {
            'name': 'Test Label',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='Test Label').exists())

    def test_update_label(self):
        response = self.client.post(reverse('label_update',
                                            kwargs={'pk': self.label.pk}),
                                    {'name': 'New Name',
                                     })
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, "New Name")
        self.assertEqual(response.status_code, 302)

    def test_delete_label(self):
        response = self.client.post(reverse("label_delete",
                                            kwargs={'pk': self.label.pk,
                                                    }))
        self.assertFalse(Label.objects.filter(pk=self.label.pk).exists())
        self.assertEqual(response.status_code, 302)