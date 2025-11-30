from rest_framework import serializers
from .models import (
    Patient,
    Appointment,
    ElectronicMedicalRecord,
    Invoice,
    InsuranceClaim,
    DemoRequest,
)


class PatientRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["id", "full_name", "email", "phone", "date_of_birth", "address"]


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"


class ElectronicMedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectronicMedicalRecord
        fields = "__all__"


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = "__all__"


class InsuranceClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceClaim
        fields = "__all__"


class DemoRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemoRequest
        fields = "__all__"
