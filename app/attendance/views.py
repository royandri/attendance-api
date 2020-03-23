from rest_framework import generics, authentication, permissions
from attendance.serializers import AttendanceSerializer


class AttendanceInViewSet(generics.RetrieveUpdateAPIView):
    # Manage attendance in the database
    serializer_class = AttendanceSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        # Retrieve and return authentication user
        return self.request.user
