from django.db import models
from django.conf import settings
from users.models import Patients, Doctors


class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(Doctors, on_delete=models.SET_NULL, null=True, blank=True)
    record_date = models.DateTimeField(auto_now_add=True)
    diagnosis = models.TextField(blank=True)
    symptoms = models.TextField(blank=True)
    treatment_plan = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Medical Record"
        verbose_name_plural = "Medical Records"
        ordering = ['-record_date']

    def __str__(self):
        return f"Record for {self.patient} on {self.record_date.date()}"


class VitalSign(models.Model):
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='vital_signs')
    blood_pressure_systolic = models.IntegerField(null=True, blank=True)
    blood_pressure_diastolic = models.IntegerField(null=True, blank=True)
    heart_rate = models.IntegerField(null=True, blank=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    respiratory_rate = models.IntegerField(null=True, blank=True)
    oxygen_saturation = models.IntegerField(null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Vital Sign"
        verbose_name_plural = "Vital Signs"

    def __str__(self):
        return f"Vitals for {self.medical_record.patient} at {self.recorded_at}"


class Prescription(models.Model):
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='prescriptions')
    medication_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    instructions = models.TextField(blank=True)
    prescribed_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Prescription"
        verbose_name_plural = "Prescriptions"

    def __str__(self):
        return f"{self.medication_name} - {self.dosage}"


class LabOrder(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE, related_name='lab_orders')
    doctor = models.ForeignKey(Doctors, on_delete=models.SET_NULL, null=True)
    test_name = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    result = models.TextField(blank=True, null=True)
    result_date = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Lab Order"
        verbose_name_plural = "Lab Orders"
        ordering = ['-ordered_date']

    def __str__(self):
        return f"{self.test_name} for {self.patient}"
