from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,logout,login
from .models import *
import datetime
import uuid
import random
from django.db.models import Avg,Sum,Count,Min,Max

from datetime import timedelta


# Create your views here.

def access(user):
    try:
        user = Doctor.objects.get(user=user)
        if user.status == "pending":
            return False
        else:
            return True
    except:
         pass



def patient_dashboard(request):
    pat = Appointment.objects.filter(patient=Patient.objects.get(user=request.user))
    d = {'data':pat}
    return render(request,'patient/patient_dashboard.html',d)

def all_doctor_appointment(request):
    pat = Appointment.objects.filter(patient=Patient.objects.get(user=request.user))
    d = {'data':pat}
    return render(request,'patient/all_doctor_appointment.html',d)

def all_patient_appointment(request):
    pat = Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user))
    d = {'data':pat}
    return render(request,'doctor/all_patient_appointment.html',d)

def doctor_dashboard(request):
    tod = datetime.date.today()
    data = Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user))
    pend = Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user),status="pending")
    c = Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user)).count()
    up = Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user), a_date__gte=tod).exclude(a_date=tod)
    today = Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user), a_date=tod)
    t_today = today.count()
    t_pending = pend.count()
    d = {'data': data, 'total': c, 'up': up, 'today': today,'t_today':t_today,'t_pending':t_pending}
    return render(request,'doctor/doctor_dashboard.html',d)

def home(request):
    data=Doctor.objects.all()
    doc = ""
    if request.method == "POST":
        l = request.POST['loc']
        s = request.POST['spe']
        if l and s:
            doc  = Doctor.objects.filter(cl_address__icontains = l,specialist__icontains = s)
        elif not l and s:
            doc  = Doctor.objects.filter(specialist__icontains = s)
        elif l and not s:
            doc  = Doctor.objects.filter(cl_address__icontains = l)
        else:
            doc = Doctor.objects.all()
    try:
        user = User.objects.get(username=request.user)
        error = Patient.objects.get(user=user)
        return redirect('patient_dashboard')
    except:
        try:
            user = User.objects.get(username=request.user)
            error = Doctor.objects.get(user=user)
            return redirect('doctor_dashboard')
        except:

            try:
                        user = User.objects.get(username=request.user)
                        if user.is_staff:
                            return redirect('admin_dashboard')
            except:
                        pass
    d={'data':data,'doc':doc}
    return render(request,'index.html',d)

def Registeration(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            m = request.POST['mode']
            if m == "Patient":
                Patient.objects.create(user=user)
            if m == "Doctor":
                Doctor.objects.create(user=user)

            messages.success(request,'You have Registered Successfully')
            return redirect('login')
    else:
        form = SignUpForm()
    d = {'form':form}
    return render(request,'register.html',d)

def Login(request):
    if request.method == "POST":
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(username=u,password=p)
        if user is not None:
            login(request,user)
            messages.success(request,'Logged in Successfully')
            return redirect('home')
        else:
            messages.success(request,'Invalid Credential')
            return redirect('login')
    return render(request,'login.html')

def Logout(request):
    logout(request)
    messages.info(request,'You have logged out successfully')
    return redirect('login')

def Patient_Profile(request):
    user = User.objects.get(id=request.user.id)
    pat = Patient.objects.get(user=user)
    form = PatientForm(request.POST or None,instance=pat)
    if request.method == "POST":
        form = PatientForm(request.POST,request.FILES,instance=pat)
        if form.is_valid():
            form.save()
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.save()
            messages.success(request,'Profile Updated Successfully')
            return redirect("patient_profile")
    d = {'form':form}
    return render(request,'patient/profile.html',d)

def Change_Password(request):
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        d = request.POST['pwd3']
        if c == d:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(d)
            u.save()
            messages.success(request,'Password Changed Successfully')
            return redirect("change_password")
    return render(request,'patient/change_password.html')

def Doctor_Profile(request):
    user = User.objects.get(id=request.user.id)
    pat = Doctor.objects.get(user=user)
    form = DoctorForm(request.POST or None,instance=pat)
    if request.method == "POST":
        form = DoctorForm(request.POST or None,request.FILES or None, instance=pat)
        if form.is_valid():
            form.save()
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.save()
            messages.success(request,'Profile Updated Successfully')
            return redirect("doctor_profile")
    d = {'doc':pat,'form':form}
    return render(request,'doctor/profile.html',d)

def Doctor_Change_Password(request):
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        d = request.POST['pwd3']
        if c == d:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(d)
            u.save()
            messages.success(request,'Password Changed Successfully')
            return redirect("change_password")
    return render(request,'doctor/change_password.html')

def payment_success(request,pid):
    data = Appointment.objects.get(id=pid)
    d={'data':data}
    return render(request,'patient/booking-success.html',d)

def search_doctor(request):
    data = Doctor.objects.all()
    l = "All"
    g = "All"
    s = "All"
    if request.method == "POST":
        l = ""
        s = ""
        g = ""
        try:
            l = request.POST['location']
        except:
            pass
        try:
            g = request.POST['gender_type']
        except:
            pass
        try:
            s = request.POST['specialist']
        except:
            pass
        data = Doctor.objects.filter(gender__icontains=g,specialist__icontains=s,cl_address__icontains=l)
    d={'data':data,'l':l,'g':g,'s':s}
    return render(request,'patient/search_doctor.html',d)

def appointment(request,pid):
    doctor=Doctor.objects.get(id=pid)
    if request.method == "POST":
        a = request.POST['a_date']
        b = request.POST['a_timing']
        app=Appointment.objects.create(doctor=doctor,patient=Patient.objects.get(user=request.user),a_date=a, a_timing=b)
        messages.success(request,"Appointment Request Sent Successfully")
        return redirect("patient_dashboard")
    d={'doctor':doctor}
    return render(request,'patient/appointment.html',d)

def p_appoinment(request):
    data=Appointment.objects.filter(patient=Patient.objects.get(user=request.user))
    d={'data':data}
    return render(request,'patient/p_appoinment.html',d)

def d_appoinment(request):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('doctor_profile')
    data=Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user))
    d={'data':data}
    return render(request,'doctor/d_appoinment.html',d)

def update_status(request,pid):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('doctor_profile')
    data=Appointment.objects.get(id=pid)
    form=AppointmentForm(request.POST or None,instance=data)
    if request.method=="POST":
        u=request.POST['a_date']
        v=request.POST['a_timing']
        data.a_date=u
        data.a_timing=v
        data.status="confirmed"
        data.save()
        messages.success(request,"Booking Completed Successfully")
        return redirect("d_appointment")
    d={'form':form,'data':data}
    return render(request,'doctor/update_status.html',d)

def confirmed_p_appoinment(request):
    tod=datetime.date.today()
    data=Appointment.objects.filter(patient=Patient.objects.get(user=request.user),status="confirmed",a_date__gte=tod)
    d={'data':data}
    return render(request,'patient/confirmed_p_appoinment.html',d)

def confirmed_d_appoinment(request):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('doctor_profile')
    tod=datetime.date.today()
    data=Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user),status="confirmed",a_date__gte=tod)
    d={'data':data}
    return render(request,'doctor/confirmed_d_appoinment.html',d)

def history_p_appoinment(request):
    tod=datetime.date.today()
    data=Appointment.objects.filter(patient=Patient.objects.get(user=request.user),a_date__lte=tod)
    d={'data':data}
    return render(request,'patient/history_p_appoinment.html',d)

def history_d_appoinment(request):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('doctor_profile')
    tod=datetime.date.today()
    data=Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user),a_date__lte=tod)
    d={'data':data}
    return render(request,'doctor/history_d_appoinment.html',d)

def p_search_appoinment(request):
    data=""
    u = ""
    v = ""
    if request.method=="POST":
        u=request.POST['from_date']
        v=request.POST['to_date']
        i1 = datetime.datetime.fromisoformat(u)
        i2 = datetime.datetime.fromisoformat(v)
        data = Appointment.objects.filter(patient=Patient.objects.get(user=request.user),a_date__gte=datetime.date(i1.year,i1.month,i1.day),a_date__lte=datetime.date(i2.year,i2.month,i2.day))
    d={'data':data,'u':u,'v':v}
    return render(request,'patient/p_search_appoinment.html',d)

def d_search_appoinment(request):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('doctor_profile')
    data=""
    u = ""
    v = ""
    if request.method=="POST":
        u=request.POST['from_date']
        v=request.POST['to_date']
        i1 = datetime.datetime.fromisoformat(u)
        i2 = datetime.datetime.fromisoformat(v)
        data = Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user),a_date__gte=datetime.date(i1.year,i1.month,i1.day),a_date__lte=datetime.date(i2.year,i2.month,i2.day))
    d={'data':data,'u':u,'v':v}
    return render(request,'doctor/d_search_appoinment.html',d)


def Login_Admin(request):
    error = False
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        if user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            error = True
    d = {'error': error}

    return render(request, 'login.html', d)

def admin_dashboard(request):
    t_doc = Doctor.objects.all().count()
    t_pat = Patient.objects.all().count()
    '''
    t_hos = Hospital_Appointment.objects.all().count()
    '''
    t_app2 = Appointment.objects.all().count()
    d = {'t_doc':t_doc,'t_pat':t_pat,'t_app2':t_app2}
    return render(request,'admin/admin_dashboard.html',d)

def admin_view_appointment(request):
    data=Appointment.objects.all()
    d={'data':data}
    return render(request,'admin/admin_view_appointment.html',d)


def admin_view_doctors(request):
    data=Doctor.objects.all()
    d={'data':data}
    return render(request,'admin/admin_view_doctors.html',d)

def admin_view_patients(request):
    data=Patient.objects.all()
    d={'data':data}
    return render(request,'admin/admin_view_patients.html',d)

def cancel_appointment(request,pid):
    pat = Appointment.objects.get(id=pid)
    pat.delete()
    messages.success(request,'Appointment Cancelled Successfully')
    return redirect('p_appoinment')


def doctor_cancel_appointment(request,pid):
    pat = Appointment.objects.get(id=pid)
    pat.delete()
    messages.success(request,'Appointment Cancelled Successfully')
    return redirect('all_patient_appointment')

def doctor_status(request,pid):
    pat = Doctor.objects.get(id=pid)
    if pat.status=="pending":
        pat.status = "accept"
        pat.save()
        messages.success(request,'Selected Doctor granted to Permission')
    else:
        pat.status = "pending"
        pat.save()
        messages.success(request, 'Selected Doctor Withdraw to Permission')
    return redirect('admin_view_doctors')


def admin_profile(request):
    return render(request,'admin/profile.html')

def edit_admin_profile(request):
    data = Adminstration.objects.get(id=request.user.id)
    if request.method == "POST":
        try:
            f = request.POST['fname']
            l = request.POST['lname']

            e = request.POST['email']

        except:
            pass
            data.user.first_name = f
            data.user.last_name = l
            data.user.email = e

            data.user.save()
            data.save()
            messages.success(request,'Profile Updated Successfully')

    try:
            n = request.POST['pwd1']
            c = request.POST['pwd2']
            d = request.POST['pwd3']
            if c == d:
                u = User.objects.get(username__exact=request.user.username)
                u.set_password(d)
                u.save()
                messages.success(request, 'Password Changed Successfully')
    except:
            pass
    return redirect('admin_profile')

def my_patient(request):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('doctor_profile')
    data = Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user),status="confirmed")
    d = {'data':data}
    return render(request,'doctor/my_patient.html',d)

def doc_patient_dashboard(request,pid):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('doctor_profile')
    data = Patient.objects.get(id=pid)
    data2 = Doctor.objects.get(user=request.user)
    pat = Appointment.objects.filter(patient = data)
    pat2 = Appointment.objects.filter(patient = data,doctor=data2,a_date = datetime.date.today()).first()
    if not pat2:
        pat2 = 0
    else:
        pat2 = pat2.id
    d = {'data': pat,'pat':data,'pat2':pat2}
    return render(request,'doctor/doc_patient_dashboard.html',d)

