from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.api.views import UserViewSet, DoctorViewSet, PatientViewSet, SpecialtyViewSet
from doctors.api.views import CategoryViewSet, BlogViewSet, CommentViewSet
from patients.api.views import AppointmentViewSet, StatusViewSet, TimeViewSet
from emr.api.views import MedicalRecordViewSet, VitalSignViewSet, PrescriptionViewSet, LabOrderViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'patients', PatientViewSet)
router.register(r'specialties', SpecialtyViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'blogs', BlogViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'statuses', StatusViewSet)
router.register(r'times', TimeViewSet)
router.register(r'medical-records', MedicalRecordViewSet)
router.register(r'vital-signs', VitalSignViewSet)
router.register(r'prescriptions', PrescriptionViewSet)
router.register(r'lab-orders', LabOrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]
