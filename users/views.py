import uuid
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

from .models import Address, Doctors, Patients, Specialty, Reste_token
from .forms import RegistrationForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from core.services import EmailService, UserService
from core.constants import TemplateName, MessageLevel

User = get_user_model()


def register(request):
    specialities = Specialty.objects.all()
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                address = Address.objects.create(
                    address_line=cd['address_line'],
                    region=cd['region'],
                    city=cd['city'],
                    code_postal=cd['pincode'],
                )
                user = User.objects.create_user(
                    first_name=cd['first_name'],
                    last_name=cd['last_name'],
                    profile_avatar=cd.get('profile_pic') or '',
                    username=cd['username'],
                    email=cd['email'],
                    gender=cd['gender'],
                    birthday=cd['birthday'],
                    password=cd['password'],
                    id_address=address,
                    is_doctor=(cd['user_config'] == 'Doctor'),
                )
                if cd['user_config'] == 'Doctor':
                    specialty = Specialty.objects.get(name=cd['Speciality'])
                    Doctors.objects.create(user=user, specialty=specialty, bio=cd.get('bio', ''))
                else:
                    Patients.objects.create(user=user, insurance=cd.get('insurance', ''))

                messages.success(request, 'Account created successfully. Please login.', extra_tags=MessageLevel.SUCCESS)
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

    return render(request, TemplateName.REGISTER, {'specialities': specialities, 'form': form})


def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user:
                login(request, user)
                if user.is_doctor:
                    return redirect('doctor_dashboard')
                return redirect('patient_dashboard')
            messages.error(request, 'Incorrect username or password')
    return render(request, TemplateName.LOGIN, {'form': form})


def forgot_view(request):
    form = ForgotPasswordForm()
    context = {'form': form}

    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = UserService.get_or_none(User, email=email)
            if user:
                token = str(uuid.uuid4())
                Reste_token.objects.create(user=user, email=email, token=token)
                if EmailService.send_password_reset(email, token):
                    context['send_email_succes'] = 1
                    messages.success(request, 'Password reset email sent.')
                else:
                    context['errorlogin'] = 1
                    messages.error(request, 'Failed to send email. Please try again.')
            else:
                context['errorlogin'] = 1
                messages.error(request, 'No account found with that email.')
        context['form'] = form

    return render(request, TemplateName.FORGOT_PASSWORD, context)


def reset_view(request, token):
    form = ResetPasswordForm()
    context = {'token': token, 'form': form}

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            reset = UserService.get_or_none(Reste_token, token=token)
            if reset:
                user = UserService.get_or_none(User, email=reset.email)
                if user:
                    user.password = make_password(form.cleaned_data['password'])
                    user.save(update_fields=['password'])
                    reset.delete()
                    messages.success(request, 'Password reset successfully. Please login.')
                    return redirect('login')
            context['errorlogin'] = 1
            messages.error(request, 'Invalid or expired reset token.')
        context['form'] = form

    return render(request, TemplateName.RESET_PASSWORD, context)


@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return redirect('login')
