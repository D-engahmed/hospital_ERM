from django.db import models
from django.utils import timezone
from users import models as user_auth_models

NOTIFICATION_TYPE_CHOICES = [
    ("general", "General"),
    ("appointment_reminder", "Appointment Reminder"),
    ("new_appointment", "New Appointment"),
    ("cancellation", "Cancellation"),
    ("rescheduling", "Rescheduling"),

]

class Doctor(models.Model):
    user = models.OneToOneField(user_auth_models.User, on_delete=models.CASCADE)
    image = models.FileField(upload_to='doctor_images/', null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    mobile = models.CharField(max_length=255, null=True, blank=True )
    country = models.CharField(max_length=255, null=True, blank=True )
    bio = models.CharField(max_length=255, null=True, blank=True )
    specialization = models.CharField(max_length=255, null=True, blank=True )
    qualification = models.CharField(max_length=255, null=True, blank=True )
    years_of_experience = models.CharField(max_length=255, null=True, blank=True )
    next_available_appointment_time = models.CharField(max_length=255, null=True, blank=True )
    
    def __str__(self):
        return f"Dr.{self.full_name}"
    
    
class Notification(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    appointment = models.ForeignKey("base.Appointment", on_delete=models.CASCADE,null=True, blank=True,related_name="doctor_appointment_notification")
    type = models.CharField(max_length=255, choices=NOTIFICATION_TYPE_CHOICES, default="general")
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural="Notifications"
    
    def __str__(self):
        return f"Dr.{self.doctor.full_name}  Notification - {self.type} "