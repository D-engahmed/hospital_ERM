from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from typing import Optional, Tuple, Any

from core.constants import AppointmentStatus, Pagination

User = get_user_model()


class PaginationService:
    @staticmethod
    def paginate(queryset: QuerySet, page: Optional[str], per_page: int = Pagination.BLOGS_PER_PAGE) -> Tuple[Any, Any]:
        paginator = Paginator(queryset, per_page)
        try:
            page_obj = paginator.get_page(page)
        except (PageNotAnInteger, EmptyPage):
            page_obj = paginator.get_page(1)
        return paginator, page_obj


class UserService:
    @staticmethod
    def get_base_template(user) -> str:
        return 'doctors/base.html' if user.is_doctor else 'patients/base.html'

    @staticmethod
    def get_or_none(model_class, **kwargs):
        try:
            return model_class.objects.get(**kwargs)
        except model_class.DoesNotExist:
            return None

    @staticmethod
    def get_user_profile(user):
        if user.is_doctor:
            return get_object_or_404(User, id=user.id), 'doctors/profile.html'
        return get_object_or_404(User, id=user.id), 'patients/profile.html'


class AppointmentService:
    @staticmethod
    def filter_appointments(queryset: QuerySet, **filters) -> QuerySet:
        qs = queryset.select_related(
            'doctor__user', 'patient__user', 'status', 'time'
        )
        filter_status = filters.get('status')
        filter_date = filters.get('date')
        filter_name = filters.get('name')

        if filter_status and filter_status != 'All':
            qs = qs.filter(status__status=filter_status)
        if filter_date:
            qs = qs.filter(start_date=filter_date)
        if filter_name:
            qs = qs.filter(
                patient__user__first_name__icontains=filter_name
            ) if filters.get('type') == 'doctor' else qs.filter(
                doctor__user__first_name__icontains=filter_name
            )
        return qs

    @staticmethod
    def update_appointment_status(appointment_id: int, new_status: str) -> None:
        from patients.models import Appointment, Status
        app = get_object_or_404(Appointment, id=appointment_id)
        status_obj = get_object_or_404(Status, status=new_status)
        app.status = status_obj
        app.save(update_fields=['status'])

    @staticmethod
    def get_doctor_appointments(doctor) -> QuerySet:
        return Appointment.objects.filter(doctor=doctor).select_related(
            'patient__user', 'status', 'time'
        )

    @staticmethod
    def get_patient_appointments(patient) -> QuerySet:
        return Appointment.objects.filter(patient=patient).select_related(
            'doctor__user', 'doctor__specialty', 'status', 'time'
        )


class BlogService:
    @staticmethod
    def get_published_blogs() -> QuerySet:
        from doctors.models import Blogs
        return Blogs.objects.filter(is_published=True).select_related(
            'doctor__user', 'id_category'
        ).order_by('-posted_at')

    @staticmethod
    def get_doctor_blogs(doctor) -> QuerySet:
        from doctors.models import Blogs
        return Blogs.objects.filter(doctor=doctor).select_related('id_category').order_by('-posted_at')

    @staticmethod
    def search_blogs(keyword: str) -> QuerySet:
        from doctors.models import Blogs
        return Blogs.objects.filter(
            title__icontains=keyword, is_published=True
        ).select_related('doctor__user', 'id_category').order_by('-posted_at')

    @staticmethod
    def get_blogs_by_category(category) -> QuerySet:
        from doctors.models import Blogs
        return Blogs.objects.filter(
            id_category=category, is_published=True
        ).select_related('doctor__user').order_by('-posted_at')

    @staticmethod
    def get_related_blogs(blog, exclude_id: int, limit: int = 3) -> QuerySet:
        from doctors.models import Blogs
        return Blogs.objects.filter(
            id_category=blog.id_category, is_published=True
        ).exclude(blog_id=exclude_id).order_by('-posted_at')[:limit]

    @staticmethod
    def get_recent_blogs(exclude_id: int, limit: int = 5) -> QuerySet:
        from doctors.models import Blogs
        return Blogs.objects.filter(is_published=True).exclude(
            blog_id=exclude_id
        ).order_by('-posted_at')[:limit]


class DoctorService:
    @staticmethod
    def get_doctor_stats(doctor):
        from doctors.models import Blogs
        from patients.models import Appointment

        total_blogs = Blogs.objects.filter(doctor=doctor).count()
        published_blogs = Blogs.objects.filter(doctor=doctor, is_published=True).count()
        draft_blogs = total_blogs - published_blogs

        total_appointments = Appointment.objects.filter(doctor=doctor).count()
        accepted = Appointment.objects.filter(doctor=doctor, status__status=AppointmentStatus.ACCEPTED.value).count()
        waited = Appointment.objects.filter(doctor=doctor, status__status=AppointmentStatus.WAITED.value).count()
        cancelled = Appointment.objects.filter(doctor=doctor, status__status=AppointmentStatus.CANCELLED.value).count()

        from datetime import date
        today_appointments = Appointment.objects.filter(
            doctor=doctor, start_date=date.today()
        ).select_related('patient__user', 'status', 'time')

        from django.db.models import Count
        current_month = date.today().month
        appointments_per_day = Appointment.objects.filter(
            doctor=doctor, start_date__month=current_month
        ).values('start_date').annotate(count=Count('start_date')).order_by('start_date')

        return {
            'total_blogs': total_blogs,
            'published_blogs': published_blogs,
            'draft_blogs': draft_blogs,
            'total_appointments': total_appointments,
            'accepted_appointments': accepted,
            'waited_appointments': waited,
            'cancelled_appointments': cancelled,
            'today_appointments': today_appointments,
            'appointments_per_day': appointments_per_day,
        }

    @staticmethod
    def filter_doctors(**filters) -> QuerySet:
        from users.models import Doctors
        qs = Doctors.objects.select_related('user__id_address', 'specialty').all()

        speciality = filters.get('speciality')
        city = filters.get('city')
        name = filters.get('name')

        if speciality and speciality != 'All':
            qs = qs.filter(specialty__name=speciality)
        if name:
            qs = qs.filter(user__first_name__icontains=name)
        if city:
            qs = qs.filter(user__id_address__city__icontains=city)
        return qs


class EmailService:
    @staticmethod
    def send_password_reset(email: str, token: str) -> bool:
        from django.core.mail import send_mail
        from django.conf import settings

        subject = 'Password Reset - Hospital ERM'
        reset_url = f'{settings.BASE_URL}/reset/{token}/'
        message = f'''
Hello,

You requested a password reset for your Hospital ERM account.

Click the link below to reset your password:
{reset_url}

If you did not request this, please ignore this email.

Regards,
Hospital ERM Team
'''
        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
            return True
        except Exception:
            return False
