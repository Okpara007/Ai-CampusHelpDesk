from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

User = get_user_model()

class CustomUserModelTest(TestCase):

    def test_user_creation(self):
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )
        self.assertEqual(user.email, 'testuser@example.com')

    def test_unique_email(self):
        # Use a different email address here to ensure uniqueness
        user1 = User.objects.create_user(
            username='testuser1',
            email='testuser1@example.com',
            password='testpassword123'
        )
        # This should raise an IntegrityError if the email is not unique
        with self.assertRaises(IntegrityError):
            user2 = User.objects.create_user(
                username='testuser2',
                email='testuser1@example.com',  # This email is the same as for user1
                password='testpassword123'
            )
