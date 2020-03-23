from django.urls import path
from attendance import views

app_name = 'attendance'

urlpatterns = [
    path(
        'attendance_in/<int:id>/',
        views.AttendanceInViewSet.as_view(),
        name='attendance-in'
    ),
]
