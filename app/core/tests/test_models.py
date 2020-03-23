from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from django.utils import timezone


def sample_user(email='test@mail.com', password='testpass'):
    # Create a sample user
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successfull(self):
        # Test creatiing a new user with an email is successfull
        email = 'royandri.dev@gmail.com'
        password = 'admin'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        # Test the email form a new user is normalized
        email = 'royandri@GMAIL.COM'
        user = get_user_model().objects.create_user(email, 'admin')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        # Test creating user with no email raises error
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'admin')

    def test_create_new_superuser(self):
        # Test creating a new superuser
        user = get_user_model().objects.create_superuser(
            'royandri.dev@gmail.com',
            'admin'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_attendance_str(self):
        # Test the attendance representation
        attendance = models.Attendance.objects.create(
            user=sample_user(),
            time_in=timezone.localtime(timezone.now()).strftime('%H:%M:%S'),
            date_in=timezone.localtime(timezone.now()).strftime('%Y-%m-%d')
        )
        self.assertEqual(str(attendance), attendance.date_in)
