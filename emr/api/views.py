from rest_framework import viewsets, permissions
from emr.models import MedicalRecord, VitalSign, Prescription, LabOrder
from .serializers import MedicalRecordSerializer, VitalSignSerializer, PrescriptionSerializer, LabOrderSerializer


class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return MedicalRecord.objects.all()
        if user.is_doctor:
            return MedicalRecord.objects.filter(doctor__user=user)
        return MedicalRecord.objects.filter(patient__user=user)


class VitalSignViewSet(viewsets.ModelViewSet):
    queryset = VitalSign.objects.all()
    serializer_class = VitalSignSerializer
    permission_classes = [permissions.IsAuthenticated]


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]


class LabOrderViewSet(viewsets.ModelViewSet):
    queryset = LabOrder.objects.all()
    serializer_class = LabOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return LabOrder.objects.all()
        if user.is_doctor:
            return LabOrder.objects.filter(doctor__user=user)
        return LabOrder.objects.filter(patient__user=user)
