from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
# from rest_framework import status
from rest_framework.test import APIClient
from core.models import Attendance, User
from django.utils import timezone
# from attendance.serializers import AttendanceSerializer


def attendance_in_url(user_id):
    # Return URL for attendance in
    return reverse('attendance:attendance-in', args=[user_id])


class AttendanceApiTest(TestCase):
    # Test attendance for user

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@mail.com',
            'testpass'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_attendance_in(self):
        # Test attendance for in user
        user = User.objects.filter(id=self.user.id)
        attendance = Attendance.objects.filter(
            user_id=self.user.id,
            date_in=timezone.localtime(timezone.now()).strftime('%Y-%m-%d')
        )
        self.assertTrue(len(user) > 0)
        self.assertFalse(len(attendance) > 0)

    def test_attendance_out(self):
        # Test attendance for out user
        user = User.objects.filter(id=self.user.id)
        attendance = Attendance.objects.filter(
            user_id=self.user.id,
            date_in=timezone.localtime(timezone.now()).strftime('%Y-%m-%d')
        )
        self.assertTrue(len(user) > 0)
        self.assertFalse(len(attendance) > 0)
