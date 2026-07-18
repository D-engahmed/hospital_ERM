from rest_framework import viewsets, permissions
from users.models import Users, Doctors, Patients, Specialty
from .serializers import UserSerializer, DoctorSerializer, PatientSerializer, SpecialtySerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Users.objects.all()
        return Users.objects.filter(id=self.request.user.id)


class DoctorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Doctors.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]


class PatientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Patients.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]


class SpecialtyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    permission_classes = [permissions.AllowAny]
