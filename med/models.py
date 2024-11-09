# models.py
from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import User

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.user.username

#patient model


#department model
class Department(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name



#doctor model
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor')  # Link to the User model
    name = models.CharField(max_length=255)
    level = models.CharField(max_length=100)  # e.g., Junior, Senior, etc.
    status = models.CharField(max_length=100)  # e.g., Active, Inactive
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    department = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255, blank=True, null=True)
    is_approved = models.BooleanField(default=False)  # To track if the doctor is approved by admin
    created_at = models.DateTimeField(auto_now_add=True)  # When the doctor was added
    updated_at = models.DateTimeField(auto_now=True)  # When the doctor information was last updated

    def __str__(self):
        return f"{self.name} - {self.level}"

    # Additional fields for the doctor's dashboard:
    # Additional fields for the doctor's dashboard:
    @property
    def total_patients(self):
        return self.patients.count()  # Use 'patients' instead of 'patient_set'

    @property
    def active_patients(self):
        return self.patients.filter(is_admitted=True).count()

    @property
    def past_patients(self):
        return self.patients.filter(is_admitted=False).count()

    @property
    def todays_appointments(self):
        today = datetime.now().date()
        return self.appointment_set.filter(date__date=today)

    @property
    def upcoming_appointments(self):
        return self.appointment_set.filter(date__gte=datetime.now())

    @property
    def weekly_appointments(self):
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        return self.appointment_set.filter(date__gte=start_of_week).count()

    @property
    def monthly_appointments(self):
        today = datetime.now()
        start_of_month = today.replace(day=1)
        return self.appointment_set.filter(date__gte=start_of_month).count()

    @property
    def new_appointments(self):
        return self.appointment_set.filter(status='requested').count()

    @property
    def patient_reviews(self):
        return self.patientreview_set.all()

class Patient(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    is_admitted = models.BooleanField(default=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='patients')  # Reverse relation
    # Other fields as required

    def __str__(self):
        return self.name

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.CharField(max_length=100, choices=[('requested', 'Requested'), ('confirmed', 'Confirmed'), ('completed', 'Completed')])

    def __str__(self):
        return f"Appointment with {self.doctor.name} on {self.date}"

class PatientReview(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.PositiveIntegerField()  # Rating out of 5

    def __str__(self):
        return f"Review by {self.patient.name} for Dr. {self.doctor.name}"
