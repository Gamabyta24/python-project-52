from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Status


class StatusCRUDTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        # Create a test status
        self.status = Status.objects.create(name="Test Status")

        # Login URL with next parameter for redirecting back after login
        self.login_url = reverse("login")

    def test_status_list_view_requires_login(self):
        # Test that status list requires login
        response = self.client.get(reverse("statuses"))
        self.assertRedirects(
            response, f'{self.login_url}?next={reverse("statuses")}'
        )

        # Login and try again
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("statuses"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "statuses/index.html")

    def test_status_create_view(self):
        # Test that status creation requires login
        response = self.client.get(reverse("status_create"))
        self.assertRedirects(
            response, f'{self.login_url}?next={reverse("status_create")}'
        )

        # Login and test creation
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("status_create"))
        self.assertEqual(response.status_code, 200)

        # Test creating a new status
        response = self.client.post(
            reverse("status_create"), {"name": "New Status"}
        )
        self.assertRedirects(response, reverse("statuses"))

        # Check that the status was created
        self.assertTrue(Status.objects.filter(name="New Status").exists())

    def test_status_update_view(self):
        # Test that status update requires login
        response = self.client.get(
            reverse("status_update", args=[self.status.id])
        )
        next_url = reverse("status_update", args=[self.status.id])
        self.assertRedirects(response, f"{self.login_url}?next={next_url}")

        # Login and test update
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("status_update", args=[self.status.id])
        )
        self.assertEqual(response.status_code, 200)

        # Test updating a status
        response = self.client.post(
            reverse("status_update", args=[self.status.id]),
            {"name": "Updated Status"},
        )
        self.assertRedirects(response, reverse("statuses"))

        # Check that the status was updated
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, "Updated Status")

    def test_status_delete_view(self):
        # Test that status deletion requires login
        response = self.client.get(
            reverse("status_delete", args=[self.status.id])
        )
        next_url = reverse("status_delete", args=[self.status.id])
        self.assertRedirects(response, f"{self.login_url}?next={next_url}")

        # Login and test deletion
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("status_delete", args=[self.status.id])
        )
        self.assertEqual(response.status_code, 200)

        # Test deleting a status
        response = self.client.post(
            reverse("status_delete", args=[self.status.id])
        )
        self.assertRedirects(response, reverse("statuses"))

        # Check that the status was deleted
        self.assertFalse(Status.objects.filter(id=self.status.id).exists())
