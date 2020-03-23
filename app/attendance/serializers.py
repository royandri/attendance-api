from rest_framework import serializers
from core.models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    # Serializer form attendance objects

    class Meta:
        model = Attendance
        fields = ('id', 'time_in', 'date_in', 'time_out', 'date_out')
        read_only_fields = ('id',)
