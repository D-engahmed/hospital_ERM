from enum import Enum


class AppointmentStatus(str, Enum):
    WAITED = 'Waited'
    ACCEPTED = 'Accepted'
    CANCELLED = 'Cancelled'

    @classmethod
    def choices(cls):
        return [(s.value, s.value) for s in cls]


class UserRole(str, Enum):
    DOCTOR = 'Doctor'
    PATIENT = 'Patient'

    @classmethod
    def choices(cls):
        return [(r.value, r.value) for r in cls]


class Gender(str, Enum):
    MALE = 'Male'
    FEMALE = 'Female'

    @classmethod
    def choices(cls):
        return [(g.value, g.value) for g in cls]


class MessageLevel(str, Enum):
    SUCCESS = 'success'
    ERROR = 'error'
    WARNING = 'warning'
    INFO = 'info'


class Pagination:
    BLOGS_PER_PAGE = 5


class TemplateName:
    LOGIN = 'users/login.html'
    REGISTER = 'users/register.html'
    FORGOT_PASSWORD = 'users/forgot.html'
    RESET_PASSWORD = 'users/reset.html'
    DOCTOR_DASHBOARD = 'doctors/doctor_dashboard.html'
    PATIENT_DASHBOARD = 'patients/patient_dashboard.html'
    DOCTOR_PROFILE = 'doctors/profile.html'
    DOCTOR_BLOGS = 'doctors/doctor_blogs.html'
    UPLOAD_BLOG = 'doctors/upload_blog.html'
    VIEW_BLOG = 'doctors/view_blog.html'
    DOCTOR_DRAFTS = 'doctors/doctor_drafts.html'
    VIEW_APPOINTMENTS = 'doctors/viewappointments.html'
    BOOK_APPOINTMENT = 'patients/book_appointment.html'
    CONFIRM_BOOKING = 'patients/patient_confirm_book.html'
    MY_APPOINTMENTS = 'patients/my_appointments.html'


class ContextKey:
    BASE_TEMPLATE = 'base_template'
    SPECIALITIES = 'specialities'
    CATEGORIES = 'categories'
    BLOGS = 'blogs'
    APPOINTMENTS = 'appointments'
