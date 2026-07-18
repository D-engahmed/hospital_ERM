from django import forms
from django.contrib.auth import get_user_model
from .models import Users, Address, Doctors, Patients, Specialty
from datetime import date

User = get_user_model()


class DateInput(forms.DateInput):
    input_type = 'date'


class RegistrationForm(forms.Form):
    user_config = forms.ChoiceField(choices=[('Doctor', 'Doctor'), ('Patient', 'Patient')])
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    profile_pic = forms.ImageField(required=False)
    username = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=50, required=True)
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')], required=True)
    birthday = forms.DateField(required=False, widget=DateInput)
    password = forms.CharField(min_length=6, widget=forms.PasswordInput)
    conf_password = forms.CharField(widget=forms.PasswordInput)
    address_line = forms.CharField(max_length=50, required=True)
    region = forms.CharField(max_length=50, required=True)
    city = forms.CharField(max_length=50, required=True)
    pincode = forms.CharField(max_length=50, required=True)
    Speciality = forms.CharField(max_length=50, required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    insurance = forms.CharField(max_length=50, required=False)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already registered.')
        return email

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get('password')
        confirm = cleaned.get('conf_password')
        if password and confirm and password != confirm:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()


class ResetPasswordForm(forms.Form):
    password = forms.CharField(min_length=6, widget=forms.PasswordInput)
    conf_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get('password')
        confirm = cleaned.get('conf_password')
        if password and confirm and password != confirm:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'gender', 'birthday', 'profile_avatar']
        widgets = {'birthday': DateInput}

    address_line = forms.CharField(max_length=50, required=False)
    region = forms.CharField(max_length=50, required=False)
    city = forms.CharField(max_length=50, required=False)
    code_postal = forms.CharField(max_length=50, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.id_address:
            addr = self.instance.id_address
            self.fields['address_line'].initial = addr.address_line
            self.fields['region'].initial = addr.region
            self.fields['city'].initial = addr.city
            self.fields['code_postal'].initial = addr.code_postal


class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(min_length=6, widget=forms.PasswordInput)
    confirm_new_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        new = cleaned.get('new_password')
        confirm = cleaned.get('confirm_new_password')
        if new and confirm and new != confirm:
            raise forms.ValidationError('New passwords do not match.')
        return cleaned
