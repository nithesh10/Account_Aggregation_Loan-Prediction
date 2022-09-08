from distutils.command.config import config
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages

import ml
import re
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserProfileForm
from .models import Credit_history, Profile
import requests
from django.contrib.auth.hashers import make_password
import random
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from .forms import DataForm
from .models import Data
import datetime
import cibil
import config

def cibil_page(request):
    print("forwarding cibil page")
    fname=cibil.get_cibil()
    print(fname)
    context = {'fname': fname}
    return render(request, 'cibil.html', context)



def send_otp(number, message):
    url = "https://www.fast2sms.com/dev/bulk"
    api = "lp2yj3iRvqQXSeUd5CmbGfK1oFJN7tAkahungz9ExIsrPcZTYwcJCNGmV3gqohR67nurkbAXOHts0KLa"
    querystring = {"authorization": api, "sender_id": "FSTSMS",
                   "message": message, "language": "english", "route": "p", "numbers": number}
    print(querystring)
    headers = {
        'cache-control': "no-cache"
    }
    return requests.request("GET", url, headers=headers, params=querystring)

def Registration(request):
    if request.method == "POST":
        fm = UserRegistrationForm(request.POST)
        up = UserProfileForm(request.POST)
        if fm.is_valid() and up.is_valid():
            e = fm.cleaned_data['email']
            u = fm.cleaned_data['username']
            p = fm.cleaned_data['password1']
            request.session['email'] = e
            request.session['username'] = u
            request.session['password'] = p
            p_number = up.cleaned_data['phone_number']
            request.session['number'] = p_number
            otp = random.randint(1000, 9999)
            request.session['otp'] = otp
            message = f'your otp is {otp}'
            send_otp(p_number, message)
            return redirect('/registration/otp/')

    else:
        fm = UserRegistrationForm()
        up = UserProfileForm()
    context = {'fm': fm, 'up': up}
    return render(request, 'registration.html', context)


def otpRegistration(request):
    if request.method == "POST":
        u_otp = request.POST['otp']
        otp = request.session.get('otp')
        user = request.session['username']
        hash_pwd = make_password(request.session.get('password'))
        p_number = request.session.get('number')
        email_address = request.session.get('email')

        if int(u_otp) == otp:
            User.objects.create(
                username=user,
                email=email_address,
                password=hash_pwd
            )
            user_instance = User.objects.get(username=user)
            Profile.objects.create(
                user=user_instance, phone_number=p_number
            )
            request.session.delete('otp')
            request.session.delete('user')
            request.session.delete('email')
            request.session.delete('password')
            request.session.delete('phone_number')

            messages.success(request, 'Registration Successfully Done !!')

            return redirect('/login/')

        else:
            messages.error(request, 'Wrong OTP')

    return render(request, 'registration-otp.html')


def userLogin(request):

    try:
        if request.session.get('failed') > 2:
            return HttpResponse('<h1> You have to wait for 5 minutes to login again</h1>')
    except:
        request.session['failed'] = 0
        request.session.set_expiry(100)

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session['username'] = username
            request.session['password'] = password
            u = User.objects.get(username=username)
            p = Profile.objects.get(user=u)
            p_number = p.phone_number
            
            otp = random.randint(1000, 9999)
            request.session['login_otp'] = otp
            message = f'your otp is {otp}'
            send_otp(p_number, message)
            return redirect('/login/otp/')
        else:
            messages.error(request, 'username or password is wrong')
    return render(request, 'login.html')


def otpLogin(request):
    print("started loging in with otp")
    if request.method == "POST":
        username = request.session['username']
        password = request.session['password']
        otp = request.session.get('login_otp')
        u_otp = request.POST['otp']
        if int(u_otp) == otp:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print("logging in with otp")
                login(request, user)
                request.session.delete('login_otp')
                messages.success(request, 'login successfully')
                return redirect('/cibil/')
        else:
            messages.error(request, 'Wrong OTP')
    print("log in with otp")
    username = request.session['username']
    password = request.session['password']
    request.session['username'] = username
    request.session['password'] = password
    u = User.objects.get(username=username)
    p = Profile.objects.get(user=u)
    p_number = p.phone_number
    config.mobile_num=int(p_number)
    print(p_number)
    return redirect('/cibil/')


def homeotp(request):
    if request.method == "POST":
        otp = random.randint(1000, 9999)
        request.session['email_otp'] = otp
        message = f'your otp is {otp}'
        user_email = request.user.email

        send_mail(
            'Email Verification OTP',
            message,
            settings.EMAIL_HOST_USER,
            [user_email],
            fail_silently=False,
        )
        return redirect('/email-verify/')

    return render(request, 'home.html')


def email_verification(request):
    if request.method == "POST":
        u_otp = request.POST['otp']
        otp = request.session['email_otp']
        if int(u_otp) == otp:
            p = Profile.objects.get(user=request.user)
            p.email_verified = True
            p.save()
            messages.success(
                request, f'Your email {request.user.email} is verified now')
            return redirect('/')
        else:
            messages.error(request, 'Wrong OTP')

    return render(request, 'email-verified.html')


def forget_password(request):
    if request.method == "POST":
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            uid = User.objects.get(email=email)
            url = f'http://127.0.0.1:8000/change-password/{uid.profile.uuid}'
            send_mail(
                'Reset Password',
                url,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return redirect('/forget-password/done/')
        else:
            messages.error(request, 'email address is not exist')
    return render(request, 'forget-password.html')


def change_password(request, uid):
    try:
        if Profile.objects.filter(uuid=uid).exists():
            if request.method == "POST":
                pass1 = 'password1' in request.POST and request.POST['password1']
                pass2 = 'password2' in request.POST and request.POST['password2']
                if pass1 == pass2:
                    p = Profile.objects.get(uuid=uid)
                    u = p.user
                    user = User.objects.get(username=u)
                    user.password = make_password(pass1)
                    user.save()
                    messages.success(
                        request, 'Password has been reset successfully')
                    return redirect('/login/')
                else:
                    return HttpResponse('Two Password did not match')

        else:
            return HttpResponse('Wrong URL')
    except:
        return HttpResponse('Wrong URL')
    return render(request, 'change-password.html')


def home(request):
    if request.method == 'POST':
        form = DataForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard-predictions')
    else:
        form = DataForm()
    context = {
        'form': form
    }
    return render(request, 'index.html')

def registerPage(request):
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already exist')
                return render(request, 'regform.html')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already exist')
                return render(request, 'regform.html')
            else:

                # save data in db
                user = User.objects.create_user(username=username, password=password1, email=email,
                                                first_name=first_name, last_name=last_name)
                user.save();
                print('user created')
                return redirect('login')

        else:
            messages.info(request, 'Invalid Credentials')
            return render(request, 'regform.html')
        return redirect('/')
    else:
        return render(request, 'regform.html')


def loginPage(request):
    print("entered login page")
    if request.method == 'POST':
        # v = DoctorReg.objects.all()
        username = request.POST['username']
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return render(request, 'predfrom.html')
        else:
            print("else")
            messages.info(request, 'Invalid credentials')
            return render(request, 'loginform.html')
    else:
        print("not logged in")
        return render(request, 'loginform.html')


def predPage(request):
    if (request.method == 'POST'):
        applicantIncome = request.POST.get('ApplicantIncome','0')
        print("data.appincome",Data.appIncome)
        coAppIncome = request.POST.get('CoapplicantIncome','0')
        maritalStatus = request.POST.get('MaritalStatus')
        gender = request.POST.get('Gender','0')
        dependents = request.POST.get('Dependents','0')
        education = request.POST.get('Education','0')
        empy_type = request.POST.get('Self_Employed','0')
        cred_hist = request.POST.get('Credit_History','0')
        prop_type = request.POST.get('Property_Area','0')
        loanAmount = request.POST.get('LoanAmount','0')
        loanAmountTerm = request.POST.get('Loan_Amount_Term','0')
        #print('DATA = ',int(applicantIncome),coAppIncome,maritalStatus,gender,dependents,education,empy_type,cred_hist,prop_type,loanAmount,loanAmountTerm)
        data = [int(applicantIncome),int(coAppIncome),int(loanAmount),int(loanAmountTerm),int(cred_hist),int(gender == 'Female'),int(gender == 'Male'),int(maritalStatus == 'Unmarried'),
                int(maritalStatus == 'Married'),int(dependents == '0'),int(dependents == '1'),int(dependents == '2'),int(dependents == '3'),
                int(education == 'Graduate'),int(education == 'Not Graduate'),int(empy_type=='Not-Self-employed'),int(empy_type=='Self-employed'),
                int(prop_type=='Rural'),int(prop_type=='Semi-urban'),int(prop_type=='Urban')]
        
    
        print(sum(data))
        print("data")
        if sum(data) != 1:
            res = ml.output(data)
            if res == "N":
                #b=Data(client_name=Profile.user,gender=gender,mstatus=maritalStatus,dependence=dependents,education=education,self_employed=empy_type,
                #appIncome=applicantIncome,co_appIncome=coAppIncome,loan_amount=loanAmount,loan_amount_term=loanAmountTerm,credit_history=cred_hist,
                #proterty_area=prop_type,loan_status=res,date = datetime.datetime.now())
                #print("\nb",b)
                #b.save()
                return render(request,'failure.html')
            elif res == 'Y':
                #b=Data(client_name=Profile.user,gender=gender,mstatus=maritalStatus,dependence=dependents,education=education,self_employed=empy_type,
                #appIncome=applicantIncome,co_appIncome=coAppIncome,loan_amount=loanAmount,loan_amount_term=loanAmountTerm,credit_history=cred_hist,
                #proterty_area=prop_type,loan_status=res,date = datetime.datetime.now())
                #print("\nb",b)
                #b.save()
                return render(request,'success.html')
        else:
            return render(request, 'predform.html')
        
    else:
        return render(request, 'predform.html')
def predictions(request):
    print("sec",str(Data.appIncome))
    predicted_diabeties = Data.objects.all()
    print(predicted_diabeties)
    context = {
        'predicted_diabeties': predicted_diabeties
    }
    
    return render(request, 'predictions.html', context)

