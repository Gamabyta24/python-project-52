from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Label
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status

class LabelCRUDTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        # Create a test label
        self.label = Label.objects.create(name='Test Label')
        
        # Create a status for task
        self.status = Status.objects.create(name='Test Status')
        
        # Login URL with next parameter for redirecting back after login
        self.login_url = reverse('login')

    def test_label_list_view_requires_login(self):
        # Test that label list requires login
        response = self.client.get(reverse('labels'))
        self.assertRedirects(response, f'{self.login_url}?next={reverse("labels")}')
        
        # Login and try again
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/index.html')

    def test_label_create_view(self):
        # Test that label creation requires login
        response = self.client.get(reverse('label_create'))
        self.assertRedirects(response, f'{self.login_url}?next={reverse("label_create")}')
        
        # Login and test creation
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('label_create'))
        self.assertEqual(response.status_code, 200)
        
        # Test creating a new label
        response = self.client.post(reverse('label_create'), {'name': 'New Label'})
        self.assertRedirects(response, reverse('labels'))
        
        # Check that the label was created
        self.assertTrue(Label.objects.filter(name='New Label').exists())

    def test_label_update_view(self):
        # Test that label update requires login
        response = self.client.get(reverse('label_update', args=[self.label.id]))
        self.assertRedirects(response, f'{self.login_url}?next={reverse("label_update", args=[self.label.id])}')
        
        # Login and test update
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('label_update', args=[self.label.id]))
        self.assertEqual(response.status_code, 200)
        
        # Test updating a label
        response = self.client.post(reverse('label_update', args=[self.label.id]), {'name': 'Updated Label'})
        self.assertRedirects(response, reverse('labels'))
        
        # Check that the label was updated
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Updated Label')

    def test_label_delete_view(self):
        # Test that label deletion requires login
        response = self.client.get(reverse('label_delete', args=[self.label.id]))
        self.assertRedirects(response, f'{self.login_url}?next={reverse("label_delete", args=[self.label.id])}')
        
        # Login and test deletion
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('label_delete', args=[self.label.id]))
        self.assertEqual(response.status_code, 200)
        
        # Test deleting a label
        response = self.client.post(reverse('label_delete', args=[self.label.id]))
        self.assertRedirects(response, reverse('labels'))
        
        # Check that the label was deleted
        self.assertFalse(Label.objects.filter(id=self.label.id).exists())
        
    def test_cannot_delete_label_in_use(self):
        # Login
        self.client.login(username='testuser', password='testpassword')
        
        # Create a task with the label
        task = Task.objects.create(
            name='Test Task',
            description='Test description',
            status=self.status,
            creator=self.user
        )
        task.labels.add(self.label)
        
        # Try to delete the label
        response = self.client.post(reverse('label_delete', args=[self.label.id]))
        
        # Should redirect back to labels with error message
        self.assertRedirects(response, reverse('labels'))
        
        # Label should still exist
        self.assertTrue(Label.objects.filter(id=self.label.id).exists())