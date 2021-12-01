from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from health.views import *

urlpatterns = (
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('login', Login, name="login"),
    path('register', Registeration, name="register"),
    path('logout', Logout, name="logout"),
    path('cancel_appointment<int:pid>', cancel_appointment, name="cancel_appointment"),
    # path('patient_invoices<int:pid><str:task>', patient_invoices,name="patient_invoices"),

    # Admin Url
    path('admin_dashboard', admin_dashboard, name="admin_dashboard"),
    path('admin_view_appointment', admin_view_appointment, name="admin_view_appointment"),
    path('admin_view_doctors', admin_view_doctors, name="admin_view_doctors"),
    path('admin_view_patients', admin_view_patients, name="admin_view_patients"),

    path('admin_profile', admin_profile, name="admin_profile"),
    path('edit_admin_profile', edit_admin_profile, name="edit_admin_profile"),

    # Patient Url
    path('patient_dashboard', patient_dashboard, name="patient_dashboard"),
    path('patient_profile', Patient_Profile, name="patient_profile"),
    path('change_password', Change_Password, name="change_password"),
    path('search_doctor', search_doctor, name="search_doctor"),
    path('booking-success', payment_success, name="booking-success"),

    path('appointment<int:pid>', appointment, name="appointment"),
    path('p_appoinment', p_appoinment, name="p_appoinment"),
    path('confirmed_p_appoinment', confirmed_p_appoinment, name="confirmed_p_appoinment"),
    path('history_p_appoinment', history_p_appoinment, name="history_p_appoinment"),
    path('p_search_appoinment', p_search_appoinment, name="p_search_appoinment"),

    # Doctor Url
    path('doctor_dashboard', doctor_dashboard, name="doctor_dashboard"),
    path('doctor_profile', Doctor_Profile, name="doctor_profile"),
    path('doctor_change_password', Doctor_Change_Password, name="doctor_change_password"),
    path('d_appoinment', d_appoinment, name="d_appoinment"),
    path('update_status<int:pid>', update_status, name="update_status"),
    path('confirmed_d_appoinment', confirmed_d_appoinment, name="confirmed_d_appoinment"),
    path('history_d_appoinment', history_d_appoinment, name="history_d_appoinment"),
    # path('add_medicine<int:pid>', add_medicine, name="add_medicine"),
    # path('doctor_invoice<int:pid>', doctor_invoices, name="doctor_invoice"),
    path('doctor_cancel_appointment<int:pid>', doctor_cancel_appointment, name="doctor_cancel_appointment"),
    path('doc_patient_dashboard<int:pid>', doc_patient_dashboard, name="doc_patient_dashboard"),
    #path('doctor_status<int:pid>', doctor_status, name="doctor_status"),
    path('d_search_appoinment',d_search_appoinment,name="d_search_appoinment"),
    path('all_patient_appointment', all_patient_appointment, name="all_patient_appointment"),
    #path('doctor_patient_search_by_id', doctor_patient_search_by_id, name="doctor_patient_search_by_id"),
    path('my_patient', my_patient, name="my_patient"),
)

static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

