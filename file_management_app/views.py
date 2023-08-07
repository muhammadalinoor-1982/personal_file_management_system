import uuid
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail
from .models import *
import os

# Create your views here.

def dashboard(request):
    ex = exam.objects.all()
    return render(request, 'home.html', locals())

def user_login(request):
    if request.method == 'POST':
        UserName = request.POST.get('username')
        Pass = request.POST.get('password')
        if len(Pass) == 0:
            messages.error(request, 'Password should not be BLANK..!!')
            return redirect('user_login')
        user = authenticate(username=UserName, password=Pass)
        if user:
            prof = Profile.objects.get(user=user)
            if prof.is_verified == True:
                login(request, user)
                return redirect('dashboard')
            else:
                return redirect('error')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid User Name or Password....!! Please Tray again')
    return render(request, 'login.html')
# End Login

# Start Logout
def user_logout(request):
    logout(request)
    messages.info(request, 'You are logged out')
    return redirect('user_login')
# End Logout

def register(request):
    if request.method == 'POST':
        First_name = request.POST.get('first')
        Last_name  = request.POST.get('last')
        UserName   = request.POST.get('name')
        Email      = request.POST.get('email')
        Pass       = request.POST.get('pass')
        Pass1      = request.POST.get('pass1')

        if UserName is not None:

            # Start Name Validation
            for i in UserName:
                if i in ['@', '#', '$', '%', '&', '()', '=', '{}', '[]']:
                    messages.warning(request, 'Please Remove Special Characters')
                    return redirect('register')
            # End Name Validation

            # Start Name Unique
            if User.objects.filter(username=UserName).exists():
                messages.warning(request, 'Given User Name Already been Exist...!!!  Please Try Other One')
            # End Name Unique

            # Start Email Unique
            elif User.objects.filter(email=Email).exists():
                messages.warning(request, 'Given Email Already been Exist...!!!  Please Try Other One')
            # End Email Unique

            else:
                # Start Check Password Matching
                if Pass == Pass1:
                # End Check Password Matching

                    user = User.objects.create_user(
                        first_name=First_name,
                        last_name=Last_name,
                        username=UserName,
                        email=Email,
                        password=Pass)

                # Start Password Hashing
                    user.set_password(Pass)
                # End Password Hashing

                # Start Generate Token
                    auth_token = str(uuid.uuid4())
                # End Generate Token

                # Start Save Registration Credentials with a Token in the Database
                    prof_obj = Profile.objects.create(user=user, auth_token=auth_token)
                    prof_obj.save()
                # End Save Registration Credentials with a Token in the Database

                # Start Sent Email with Token
                    send_mail_reg(Email, auth_token)
                # End Sent Email with Token

                    #messages.success(request, 'Account has been created')
                    return redirect('success')
                else:
                    messages.error(request, 'Your Given Password not matched With Confirm Password')

    return render(request, 'registration.html')
# End Registration
def success(request):
    return render(request, 'success.html')

def token_send(request):
    return render(request, 'token_send.html')

def error(request):
    return render(request, 'error.html')

def send_mail_reg(Email, auth_token):
    subject = 'Your Account Authentication Link'
    message = f'Hi..!! Please Click The Link to Verify Your Account  http://127.0.0.1:8000/verify/{auth_token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)
# End Email Sending Process for Email Verification

# Start Email Verification Process
def verify(request, auth_token):
    prof_obj = Profile.objects.filter(auth_token=auth_token).first()
    prof_obj.is_verified = True
    prof_obj.save()
    messages.success(request, 'Congratulations...!!!!   Your Account has been verified')
    return redirect('user_login')
# End Email Verification Process

def ex_create(request):
    if request.method == 'POST':
        name    =request.POST.get('name')
        image   =request.FILES.get('image')
        sex     =request.POST.get('sex')

        if name:
            if image:
                ex = exam.objects.create(
                    name=name,
                    image=image,
                    sex=sex
                )
                ex.save()
                messages.success(request, 'Item Created Successfully')
                return redirect('dashboard')
            else:
                ex = exam.objects.create(
                    sex=sex
                )
                ex.save()
                messages.success(request, 'Item Created Successfully')
                return redirect('dashboard')
        else:
            messages.error(request, 'Please fill up the Field')
    return render(request, 'excreate.html', locals())

def ex_update(request, id):
    ex = exam.objects.get(id=id)
    if request.method == 'POST':
        if request.FILES.get('image') != None:
            if ex.image != 'default/no_img.jpg':
                os.remove(ex.image.path)
            ex.name     = request.POST.get('name')
            ex.image    = request.FILES.get('image')
            ex.sex      = request.POST.get('sex')
            ex.save()
            messages.success(request, 'Item Updated successfully')
            return redirect('dashboard')
        else:
            ex.name = request.POST.get('name')
            ex.sex = request.POST.get('sex')
            ex.save()
            messages.success(request, 'Item Updated successfully')
            return redirect('dashboard')
    return render(request, 'exupdate.html', locals())

def ex_delete(request, id):
    ex = exam.objects.get(id=id)
    if ex.image != 'default/no_img.jpg':
        os.remove(ex.image.path)
    ex.delete()
    messages.error(request, 'Item Deleted Successfully')
    return redirect('dashboard')






