from django.db import models


class Hospital(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Patient(models.Model):
    hospital = models.ForeignKey(
        Hospital, on_delete=models.SET_NULL, null=True, blank=True, related_name="patients"
    )
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
    doctor_name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("BOOKED", "Booked"),
            ("CANCELLED", "Cancelled"),
            ("COMPLETED", "Completed"),
        ],
        default="BOOKED",
    )
    insurance_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.full_name} - {self.doctor_name} @ {self.date} {self.time}"


class ElectronicMedicalRecord(models.Model):
    patient = models.OneToOneField(
        Patient, on_delete=models.CASCADE, related_name="emr"
    )
    active_conditions = models.TextField(blank=True)
    current_medications = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    genetic_history = models.TextField(blank=True)
    last_checkup_date = models.DateField(null=True, blank=True)
    last_glucose = models.FloatField(null=True, blank=True)
    last_cholesterol = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"EMR for {self.patient.full_name}"


class Invoice(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="invoices")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ("PENDING", "Pending"),
            ("PAID", "Paid"),
            ("CANCELLED", "Cancelled"),
        ],
        default="PENDING",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.id} - {self.patient.full_name}"


class InsuranceClaim(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="claims")
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="claims")
    policy_number = models.CharField(max_length=50)
    status = models.CharField(
        max_length=20,
        choices=[
            ("SUBMITTED", "Submitted"),
            ("APPROVED", "Approved"),
            ("DENIED", "Denied"),
        ],
        default="SUBMITTED",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Claim {self.id} - {self.patient.full_name}"


class DemoRequest(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    hospital_name = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Demo request from {self.name}"
