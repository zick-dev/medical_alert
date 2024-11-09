from django.urls import path
from . import views

urlpatterns = [
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('approve-doctor/<int:doctor_id>/', views.approve_doctor, name='approve_doctor'),
    path('admin/users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin/users/delete_all/', views.delete_all_users, name='delete_all_users'),
    path('book-appointment/', views.book_appointment, name='book-appointment'),
    path('departments/', views.departments, name='departments'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctor/<int:doctor_id>/', views.doctor_profile, name='doctor_profile'),
    path('doctors-waiting-approval/', views.doctors_waiting_approval, name='doctors_waiting_approval'),
    path('', views.login_view, name='login'),  # Home page
    #path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('payment/', views.payment, name='payment'),
    path('payroll/', views.payroll, name='payroll'),
    path('register-doctor/', views.register_doctor, name='register-doctor'),
    path('register/', views.register_patient, name='register-patient'),
    path('settings/', views.settings, name='settings'),
    path('update-settings/', views.update_settings, name='update_settings'),
    path('user-count/', views.user_count, name='user_count'),
]
