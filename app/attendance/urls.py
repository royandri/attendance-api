from django.urls import path
from attendance import views

app_name = 'attendance'

urlpatterns = [
    path(
        'attendance_in/',
        views.AttendanceInViewSet.as_view({'post': 'attendance_in'}),
        name='attendance-in'
    ),
    path(
        'attendance_out/',
        views.AttendanceInViewSet.as_view({'post': 'attendance_out'}),
        name='attendance-out'
    ),
]
