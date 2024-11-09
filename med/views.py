from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import PatientSignupForm
from .models import Patient, Department, Doctor, Appointment, PatientReview
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import DoctorSignUpForm
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db.models import Count, Q


@login_required
def admin_dashboard(request):
    total_patients = Patient.objects.count()
    admitted_patients = Patient.objects.filter(is_admitted=True).count()
    discharged_patients = Patient.objects.filter(is_admitted=False).count()
    total_departments = Department.objects.count()
    doctors_waiting_approval = Doctor.objects.filter(is_approved=False)
    departments = Department.objects.all()
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()

    context = {
        'total_patients': total_patients,
        'admitted_patients': admitted_patients,
        'discharged_patients': discharged_patients,
        'total_departments': total_departments,
        'doctors_waiting_approval': doctors_waiting_approval,
        'departments': departments,
        'doctors': doctors,
        'patients': patients,
    }
    return render(request, 'admin_dashboard.html', context)

def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return redirect('admin_dashboard.html')
    except User.DoesNotExist:
        return HttpResponse("User not found.")


@login_required
def delete_all_users(request):
    # Exclude admin users by filtering based on a condition (e.g., superuser status)
    User.objects.filter(is_superuser=False).delete()

    messages.success(request, "All non-admin users have been deleted.")
    return redirect('admin_dashboard')

def book_appointment(request):
    return render(request, 'med/book_appointment.html')


def departments(request):
    return render(request, 'med/departments.html')


@login_required
def doctor_dashboard(request):
    doctor = request.user.doctor  # Assuming user is linked to Doctor model

    # Doctor's basic info
    doctor_name = doctor.name
    doctor_level = doctor.level  # Assuming level is a field in Doctor model
    doctor_status = doctor.status  # Assuming status is a field in Doctor model
    doctor_number = doctor.phone_number  # Assuming you have a phone number field
    doctor_email = doctor.user.email
    doctor_id = doctor.id

    # Total patients and active/past patients
    total_patients = Patient.objects.filter(doctor=doctor).count()
    active_patients = Patient.objects.filter(doctor=doctor, is_admitted=True).count()
    past_patients = Patient.objects.filter(doctor=doctor, is_admitted=False).count()

    # Today's appointments and upcoming appointments
    today = datetime.now()
    todays_appointments = Appointment.objects.filter(doctor=doctor, date__date=today.date())
    upcoming_appointments = Appointment.objects.filter(doctor=doctor, date__gte=today)

    # Patient reviews
    patient_reviews = PatientReview.objects.filter(doctor=doctor)

    # Appointment statistics
    start_of_week = today - timedelta(days=today.weekday())  # Start of the current week
    start_of_month = today.replace(day=1)  # Start of the current month
    weekly_appointments = Appointment.objects.filter(doctor=doctor, date__gte=start_of_week).count()
    monthly_appointments = Appointment.objects.filter(doctor=doctor, date__gte=start_of_month).count()

    # New appointment requests
    new_appointments = Appointment.objects.filter(doctor=doctor, status='requested').count()

    context = {
        'doctor_name': doctor_name,
        'doctor_level': doctor_level,
        'doctor_status': doctor_status,
        'doctor_number': doctor_number,
        'doctor_email': doctor_email,
        'doctor_id': doctor_id,
        'total_patients': total_patients,
        'active_patients': active_patients,
        'past_patients': past_patients,
        'todays_appointments': todays_appointments,
        'upcoming_appointments': upcoming_appointments,
        'patient_reviews': patient_reviews,
        'weekly_appointments': weekly_appointments,
        'monthly_appointments': monthly_appointments,
        'new_appointments': new_appointments,
    }

    return render(request, 'med/doctor_dashboard.html', context)

def doctor_profile(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    return render(request, 'med/doctor_profile.html', {'doctor': doctor})

def doctor_list(request):
    doctors = Doctor.objects.all()  # Fetch all doctors
    return render(request, 'med/doctor_list.html', {'doctors': doctors})

@login_required
def approve_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    doctor.is_approved = True
    doctor.save()
    return HttpResponseRedirect(reverse('admin_dashboard'))

def doctors_waiting_approval(request):
    return render(request, 'med/doctors_waiting_approval.html')


def home(request):
    return render(request, 'med/home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Allows for username or email
        password = request.POST.get('password')

        # Authenticate using the custom backend
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('patient_dashboard')
        else:
            messages.error(request, "Invalid login credentials.")
            return render(request, 'med/login.html')

    return render(request, 'med/login.html')


def logout_view(request):
    return render(request, 'med/logout.html')


def patient_dashboard(request):
    return render(request, 'med/patient_dashboard.html')


def payment(request):
    return render(request, 'med/payment.html')


def payroll(request):
    return render(request, 'med/payroll.html')

def register_doctor(request):
    if request.method == 'POST':
        form = DoctorSignUpForm(request.POST)
        if form.is_valid():
            # Save the form data (doctor registration)
            user = form.save()  # Create the User

            # Create the doctor profile, marking it as awaiting admin approval
            user.doctor.is_approved = False  # Assuming you have a 'is_approved' field in the Doctor model
            user.doctor.save()

            # Inform the user that their account is created and waiting for approval
            messages.success(request, 'Your account has been created. You are waiting for admin approval.')

            # Redirect to the login page or any other appropriate page
            return redirect('login')  # Change this if you want to redirect to a different page
    else:
        form = DoctorSignUpForm()

    return render(request, 'med/register_doctor.html', {'form': form})


def register_patient(request):
    if request.method == 'POST':
        form = PatientSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('patient_dashboard')
    else:
        form = PatientSignupForm()

    return render(request, 'med/register.html', {'form': form})


def settings(request):
    return render(request, 'med/settings.html')


def update_settings(request):
    return render(request, 'med/update_settings.html')


def user_count(request):
    return render(request, 'med/user_count.html')
