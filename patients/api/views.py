from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from patients.models import Appointment, Status, Time
from .serializers import AppointmentSerializer, StatusSerializer, TimeSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_doctor:
            return Appointment.objects.filter(doctor__user=user)
        return Appointment.objects.filter(patient__user=user)

    def perform_create(self, serializer):
        from users.models import Patients
        patient = Patients.objects.get(user=self.request.user)
        status = Status.objects.get(status='Waited')
        serializer.save(patient=patient, status=status)


class StatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [permissions.AllowAny]


class TimeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Time.objects.all()
    serializer_class = TimeSerializer
    permission_classes = [permissions.AllowAny]
