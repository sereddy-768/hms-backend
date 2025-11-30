from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum

from .models import (
    Patient,
    Appointment,
    ElectronicMedicalRecord,
    Invoice,
    InsuranceClaim,
    DemoRequest,
)
from .serializers import (
    PatientRegistrationSerializer,
    PatientSerializer,
    AppointmentSerializer,
    ElectronicMedicalRecordSerializer,
    InvoiceSerializer,
    InsuranceClaimSerializer,
    DemoRequestSerializer,
)


class PatientRegistrationView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientRegistrationSerializer


class PatientListView(generics.ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class PatientDashboardSummary(APIView):
    def get(self, request, patient_id):
        try:
            patient = Patient.objects.get(pk=patient_id)
        except Patient.DoesNotExist:
            return Response({'detail': 'Patient not found'}, status=404)

        appointments = patient.appointments.all()
        invoices = patient.invoices.all()
        claims = patient.claims.all()

        data = {
            'patient_name': patient.full_name,
            'appointments_count': appointments.count(),
            'records_count': 1 if hasattr(patient, 'emr') else 0,
            'prescriptions_count': 3,
            'lab_results_count': 5,
            'next_appointment': str(
                appointments.filter(status='BOOKED').order_by('date', 'time').first()
            ) if appointments.exists() else 'No upcoming appointments',
            'notifications': [
                'New Lab Report ready.',
                'Your next appointment reminder (demo data).',
            ],
            'billing_pending': invoices.filter(status='PENDING').count(),
            'claims_submitted': claims.count(),
        }
        return Response(data)


class EMRDetailView(APIView):
    def get(self, request, patient_id):
        try:
            patient = Patient.objects.get(pk=patient_id)
        except Patient.DoesNotExist:
            return Response({'detail': 'Patient not found'}, status=404)

        emr, _ = ElectronicMedicalRecord.objects.get_or_create(patient=patient)
        serializer = ElectronicMedicalRecordSerializer(emr)
        return Response(serializer.data)

    def put(self, request, patient_id):
        try:
            patient = Patient.objects.get(pk=patient_id)
        except Patient.DoesNotExist:
            return Response({'detail': 'Patient not found'}, status=404)

        emr, _ = ElectronicMedicalRecord.objects.get_or_create(patient=patient)
        serializer = ElectronicMedicalRecordSerializer(emr, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class StaffOperationsOverview(APIView):
    def get(self, request):
        total_patients = Patient.objects.count()
        todays_appointments = Appointment.objects.count()
        doctors = Appointment.objects.values('doctor_name').distinct().count()
        departments = Appointment.objects.values('specialty').distinct().count()

        doctor_status = [
            {'name': 'Dr. Sarah Smith', 'dept': 'Cardiology', 'status': 'Available'},
            {'name': 'Dr. Priya Patel', 'dept': 'Emergency', 'status': 'On Duty'},
            {'name': 'Dr. James Johnson', 'dept': 'Pediatrics', 'status': '3 Appointments'},
        ]

        data = {
            'total_patients': total_patients,
            'todays_appointments': todays_appointments,
            'doctors': doctors,
            'departments': departments,
            'doctor_status': doctor_status,
        }
        return Response(data)


class AppointmentCreateView(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class AppointmentListView(generics.ListAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        qs = Appointment.objects.all()
        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            qs = qs.filter(patient_id=patient_id)
        return qs


class AppointmentDetailView(generics.RetrieveUpdateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class InvoiceListCreateView(generics.ListCreateAPIView):
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        qs = Invoice.objects.all()
        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            qs = qs.filter(patient_id=patient_id)
        return qs


class InsuranceClaimListCreateView(generics.ListCreateAPIView):
    serializer_class = InsuranceClaimSerializer

    def get_queryset(self):
        qs = InsuranceClaim.objects.all()
        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            qs = qs.filter(patient_id=patient_id)
        return qs


class HospitalAnalyticsView(APIView):
    def get(self, request):
        total_visits = Appointment.objects.count()
        revenue = Invoice.objects.aggregate(total=Sum('amount'))['total'] or 0
        occupancy = 75
        avg_response_time = 10
        satisfaction = 4.5
        staff_efficiency = 88

        data = {
            'total_visits': total_visits,
            'revenue': float(revenue),
            'occupancy': occupancy,
            'avg_response_time': avg_response_time,
            'satisfaction': satisfaction,
            'staff_efficiency': staff_efficiency,
        }
        return Response(data)


class DemoRequestCreateView(generics.CreateAPIView):
    queryset = DemoRequest.objects.all()
    serializer_class = DemoRequestSerializer
