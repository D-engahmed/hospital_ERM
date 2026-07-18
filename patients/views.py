from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date

from users.models import Doctors, Specialty, Patients
from .models import Appointment, Time, Status
from .forms import AppointmentForm
from core.services import AppointmentService, DoctorService
from core.constants import TemplateName, ContextKey, AppointmentStatus, MessageLevel, UserRole

User = get_user_model()


@login_required(login_url='/login')
def patient_dashboard(request):
    patient = get_object_or_404(Patients, user=request.user)
    appointments = AppointmentService.get_patient_appointments(patient)

    upcoming = appointments.filter(start_date__gte=date.today(), status__status=AppointmentStatus.ACCEPTED.value)
    total = appointments.count()
    accepted = appointments.filter(status__status=AppointmentStatus.ACCEPTED.value).count()
    pending = appointments.filter(status__status=AppointmentStatus.WAITED.value).count()

    return render(request, TemplateName.PATIENT_DASHBOARD, {
        'total_appointments': total,
        'accepted_appointments': accepted,
        'pending_appointments': pending,
        'upcoming_appointments': upcoming[:5],
    })


@login_required(login_url='/login')
def patient_profile(request):
    from users.forms import ProfileForm, PasswordChangeForm
    from django.contrib.auth import update_session_auth_hash

    profile_form = ProfileForm(instance=request.user)
    password_form = PasswordChangeForm()
    updated_profile = False
    updated_password = False

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = ProfileForm(request.POST, request.FILES, instance=request.user)
            if profile_form.is_valid():
                user = profile_form.save(commit=False)
                if request.user.id_address:
                    addr = request.user.id_address
                    addr.address_line = profile_form.cleaned_data.get('address_line', addr.address_line)
                    addr.region = profile_form.cleaned_data.get('region', addr.region)
                    addr.city = profile_form.cleaned_data.get('city', addr.city)
                    addr.code_postal = profile_form.cleaned_data.get('code_postal', addr.code_postal)
                    addr.save()
                insurance = request.POST.get('insurance', '')
                patient_profile = request.user.patients
                patient_profile.insurance = insurance
                patient_profile.save()
                user.save()
                updated_profile = True
                messages.success(request, 'Profile updated successfully.', extra_tags=MessageLevel.SUCCESS)
            else:
                for field, errors in profile_form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')

        elif 'update_password' in request.POST:
            password_form = PasswordChangeForm(request.POST)
            if password_form.is_valid():
                if not request.user.check_password(password_form.cleaned_data['current_password']):
                    messages.error(request, 'Current password is incorrect.')
                else:
                    request.user.set_password(password_form.cleaned_data['new_password'])
                    request.user.save()
                    update_session_auth_hash(request, request.user)
                    updated_password = True
                    messages.success(request, 'Password updated successfully.', extra_tags=MessageLevel.SUCCESS)
            else:
                for field, errors in password_form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')

    return render(request, TemplateName.DOCTOR_PROFILE, {
        'basicdata': request.user,
        'updated_profile_successfully': updated_profile,
        'updated_password_successfully': updated_password,
        'base_template': 'patients/base.html',
        'profile_form': profile_form,
        'password_form': password_form,
    })


@login_required(login_url='/login')
def my_appointments(request):
    patient = get_object_or_404(Patients, user=request.user)
    appointments = AppointmentService.get_patient_appointments(patient)

    filter_status = request.GET.get('filter_status')
    filter_date = request.GET.get('filter_date')
    filter_doctor_name = request.GET.get('filter_doctor_name')

    if filter_status and filter_status != 'All':
        appointments = appointments.filter(status__status=filter_status)
    if filter_date:
        appointments = appointments.filter(start_date=filter_date)
    if filter_doctor_name:
        appointments = appointments.filter(doctor__user__first_name__icontains=filter_doctor_name)

    return render(request, TemplateName.MY_APPOINTMENTS, {
        ContextKey.APPOINTMENTS: appointments,
        'filter_status': filter_status,
        'filter_date': filter_date,
        'filter_doctor_name': filter_doctor_name,
    })


@login_required(login_url='/login')
def book_appointment(request):
    specialities = Specialty.objects.all()
    doctors = DoctorService.filter_doctors(
        speciality=request.GET.get('filter_speciality'),
        city=request.GET.get('filter_city'),
        name=request.GET.get('filter_doctor_name'),
    )

    return render(request, TemplateName.BOOK_APPOINTMENT, {
        'doctors': doctors,
        ContextKey.SPECIALITIES: specialities,
        'filter_speciality': request.GET.get('filter_speciality'),
        'filter_doctor_name': request.GET.get('filter_doctor_name'),
        'filter_city': request.GET.get('filter_city'),
    })


@login_required(login_url='/login')
def patient_confirm_book(request, doctor):
    doc = get_object_or_404(Doctors, user__username=doctor)
    form = AppointmentForm()

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            try:
                appointment = form.save(commit=False)
                appointment.doctor = doc
                appointment.patient = get_object_or_404(Patients, user=request.user)
                appointment.status = get_object_or_404(Status, status=AppointmentStatus.WAITED.value)
                appointment.save()
                messages.success(request, 'Appointment booked successfully!', extra_tags=MessageLevel.SUCCESS)
                return redirect('my_appointments')
            except Exception as e:
                messages.error(request, f'Booking failed: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

    return render(request, TemplateName.CONFIRM_BOOKING, {
        'times': Time.objects.all(),
        'doctor': doc,
        'form': form,
    })
