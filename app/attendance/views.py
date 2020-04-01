from rest_framework import authentication, permissions
from attendance.serializers import AttendanceSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from core.models import Attendance, User
from django.utils import timezone
from datetime import datetime


class AttendanceInViewSet(viewsets.ModelViewSet):
    # Manage attendance in the database
    serializer_class = AttendanceSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_user(self):
        # Retrieve and return authentication user
        try:
            user = User.objects.get(id=self.request.user.id)
            return user
        except User.DoesNotExist:
            return False

    def add_attendance(self):
        # Add new attendance
        defaults = {
            'date_in': timezone.localtime(timezone.now()).strftime('%Y-%m-%d'),
            'time_in': timezone.localtime(timezone.now()).strftime('%H:%M:%S')
        }

        try:
            Attendance.objects.create(user=self.get_user(), **defaults)
            return True
        except Exception:
            return False

    def update_attendance(self, id_attendance):
        # Update attendance
        data_update = {
            'date_out': timezone.localtime(timezone.now())
                                .strftime('%Y-%m-%d'),
            'time_out': timezone.localtime(timezone.now())
                                .strftime('%H:%M:%S')
        }

        try:
            Attendance.objects.filter(id=id_attendance).update(**data_update)
            return True
        except Exception:
            return False

    def attendance_in(self, request):
        # Perform attendance in
        user = self.get_user()

        if not user:
            return Response({
                'success': 0,
                'message': "Unauthorized",
                'data': []
            }, status=status.HTTP_401_UNAUTHORIZED)

        has_attendance = Attendance.objects.filter(user=user).exists()

        if has_attendance:
            tmp_attendance = Attendance.objects.filter(user=user).last()
            if tmp_attendance.date_out is None:
                return Response({
                    'success': 0,
                    'message': "Failed, please logout last attendance",
                    'data': []
                }, status=status.HTTP_400_BAD_REQUEST)

        is_save = self.add_attendance()
        result = {
            'success': 0,
            'message': 'Attendance failed',
            'data': []
        }
        statcode = status.HTTP_400_BAD_REQUEST

        if is_save:
            result = {
                'success': 1,
                'message': "Success, you've been logged in",
                'data': []
            }
            statcode = status.HTTP_201_CREATED

        return Response(result, status=statcode)

    def attendance_out(self, request):
        # Perform attendance out

        user = self.get_user()

        if not user:
            return Response({
                'success': 0,
                'message': "Unauthorized",
                'data': []
            }, status=status.HTTP_401_UNAUTHORIZED)

        has_attendance = Attendance.objects.filter(user=user).exists()

        if has_attendance:
            tmp_attendance = Attendance.objects.filter(user=user).last()
            if tmp_attendance.date_out:
                return Response({
                    'success': 0,
                    'message': "Failed, you haven't signed in yet",
                    'data': []
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                tmp_in = tmp_attendance.date_in.strftime('%Y-%m-%d') + " " \
                         + tmp_attendance.time_in.strftime('%H:%M:%S')
                tmp_now = timezone.localtime(timezone.now()) \
                                  .strftime('%Y-%m-%d %H:%M:%S')

                datetime_in = datetime.strptime(tmp_in, '%Y-%m-%d %H:%M:%S')
                datetime_now = datetime.strptime(tmp_now, '%Y-%m-%d %H:%M:%S')
                duration = datetime_now - datetime_in
                work_time = duration.total_seconds() / 3600

                if(work_time < 8):
                    return Response({
                        'success': 0,
                        'message': "Failed, worktime are still under 8 hours",
                        'data': []
                    }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'success': 0,
                'message': "Failed, you haven't signed in yet",
                'data': []
            }, status=status.HTTP_400_BAD_REQUEST)

        last_attendance = Attendance.objects.filter(user=user).last()
        is_update = self.update_attendance(last_attendance.id)

        result = {
            'success': 0,
            'message': 'Failed logout attendance',
            'data': []
        }
        statcode = status.HTTP_400_BAD_REQUEST

        if is_update:
            result = {
                'success': 1,
                'message': "Success, you've been logout",
                'data': []
            }
            statcode = status.HTTP_200_OK

        return Response(result, status=statcode)
