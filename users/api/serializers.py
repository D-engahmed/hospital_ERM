from rest_framework import serializers
from users.models import Users, Address, Doctors, Patients, Specialty


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer(source='id_address', read_only=True)

    class Meta:
        model = Users
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'gender', 'birthday', 'is_doctor', 'profile_avatar', 'address']
        read_only_fields = ['id', 'is_doctor']


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    specialty = SpecialtySerializer(read_only=True)

    class Meta:
        model = Doctors
        fields = ['user', 'specialty', 'bio']


class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Patients
        fields = ['user', 'insurance']
