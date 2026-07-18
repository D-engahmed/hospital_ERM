from rest_framework import serializers
from emr.models import MedicalRecord, VitalSign, Prescription, LabOrder


class VitalSignSerializer(serializers.ModelSerializer):
    class Meta:
        model = VitalSign
        fields = '__all__'
        read_only_fields = ['id', 'recorded_at']


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'
        read_only_fields = ['id', 'prescribed_date']


class MedicalRecordSerializer(serializers.ModelSerializer):
    vital_signs = VitalSignSerializer(many=True, read_only=True)
    prescriptions = PrescriptionSerializer(many=True, read_only=True)

    class Meta:
        model = MedicalRecord
        fields = ['id', 'patient', 'doctor', 'record_date', 'diagnosis', 'symptoms', 'treatment_plan', 'notes', 'is_active', 'vital_signs', 'prescriptions']
        read_only_fields = ['id', 'record_date']


class LabOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabOrder
        fields = '__all__'
        read_only_fields = ['id', 'ordered_date']
