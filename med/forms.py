from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Doctor
from django.conf import settings

class PatientSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")
    password_confirmation = forms.CharField(widget=forms.PasswordInput(), label="Confirm password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirmation']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password and password_confirmation and password != password_confirmation:
            self.add_error('password_confirmation', "Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password before saving
        if commit:
            user.save()
        return user


class DoctorSignUpForm(forms.ModelForm):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Doctor
        fields = ['name', 'level', 'status', 'phone_number', 'email', 'department', 'specialty']

    # Use a CharField for department to allow text input
    department = forms.CharField(max_length=255, required=True)
    def save(self, commit=True):
        # Create the user first
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        # Now create the doctor instance, with 'is_approved' set to False
        doctor = super().save(commit=False)
        doctor.user = user  # Link the doctor with the user instance
        doctor.is_approved = False  # Pending approval
        doctor.save()  # Save the doctor instance
        return doctor
