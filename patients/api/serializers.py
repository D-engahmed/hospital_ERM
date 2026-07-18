from rest_framework import serializers
from patients.models import Appointment, Status, Time
from users.api.serializers import DoctorSerializer, PatientSerializer


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class TimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Time
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    doctor_detail = DoctorSerializer(source='doctor', read_only=True)
    patient_detail = PatientSerializer(source='patient', read_only=True)
    status_name = serializers.CharField(source='status.status', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'doctor_detail', 'patient', 'patient_detail', 'summary', 'description', 'start_date', 'status', 'status_name', 'time']
        read_only_fields = ['id']
