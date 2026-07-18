from django.contrib import admin
from .models import MedicalRecord, VitalSign, Prescription, LabOrder


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'record_date', 'is_active']
    list_filter = ['is_active', 'record_date']
    search_fields = ['patient__user__first_name', 'patient__user__last_name', 'diagnosis']


@admin.register(VitalSign)
class VitalSignAdmin(admin.ModelAdmin):
    list_display = ['medical_record', 'blood_pressure_systolic', 'heart_rate', 'temperature', 'recorded_at']


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['medication_name', 'dosage', 'frequency', 'prescribed_date', 'is_active']
    list_filter = ['is_active', 'prescribed_date']
    search_fields = ['medication_name']


@admin.register(LabOrder)
class LabOrderAdmin(admin.ModelAdmin):
    list_display = ['test_name', 'patient', 'doctor', 'ordered_date', 'is_completed']
    list_filter = ['is_completed', 'ordered_date']
