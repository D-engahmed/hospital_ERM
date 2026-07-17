from django.db import models
from django.utils import timezone
from users import models as user_auth_models

NOTIFICATION_TYPE_CHOICES = [
    ("general", "General"),
    ("appointment_reminder", "Appointment Reminder"),
    ("Scheduled_appointment", "Scheduled Appointment"),
    ("cancellation", "Cancellation"),
    ("rescheduling", "Rescheduling"),

]

class Patient(models.Model):
    user = models.OneToOneField(user_auth_models.User, on_delete=models.CASCADE)
    image = models.FileField(upload_to='patient_images/', null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    mobile = models.CharField(max_length=255, null=True, blank=True )
    address = models.CharField(max_length=255, null=True, blank=True )
    email = models.CharField(max_length=255, null=True, blank=True )
    gender = models.CharField(max_length=255, null=True, blank=True )
    date_of_barth= models.CharField(max_length=255, null=True, blank=True )
    blood_group= models.CharField(max_length=255, null=True, blank=True )
    
    def __str__(self):
        return f"{self.full_name}"
    
    
class Notification(models.Model):
    patient = models.ForeignKey(patient, on_delete=models.SET_NULL, null=True, blank=True)
    appointment = models.ForeignKey("base.Appointment", on_delete=models.CASCADE,null=True, blank=True,related_name="doctor_appointment_notification")
    type = models.CharField(max_length=255, choices=NOTIFICATION_TYPE_CHOICES, default="general")
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural="Notifications"
    
    def __str__(self):
        return f"{self.patient.full_name}  Notification - {self.type} "