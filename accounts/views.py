from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import User
from django.contrib.auth.decorators import login_required
from report.models import Report
from .forms import RegistrationForm, UserProfileForm,LoginForm
from .models import User, Profile, Department
from django.contrib import messages,auth
from django.contrib.auth import authenticate,login
# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


# Login view
def login(request):    
    if request.method == 'POST':
        form = LoginForm(data=request.POST)    
        
        if form.is_valid():
            user = form
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(form=form,email=email, password=password)                                  
            
        if user is not None:            
            auth.login(request,user)
            if user.is_superadmin == True:
                messages.success(request, 'You are logged in')
                return redirect('superadmin')
            messages.success(request, 'You are logged in')    
            return redirect('dashboard')    
        else:
            form = LoginForm()
            
            messages.error(request, 'Unable to login, Check your email and password')
            return redirect('login')        
    else:
        form = LoginForm()
    context = {
        'form':form
    }    
    return render(request, 'accounts/user/login.html',context)


# Log out view
@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are now logged out.')
    return redirect('login')


# User registration view
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            department = form.cleaned_data['department']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)

            if User.objects.filter(email = user.email).exists():
                    messages.warning(request, 'Email Already exists, Please use a different email')
                    return redirect('register')
            user.department = department
            user.phone_number = phone_number
            user.is_active = True
            user.save()
            
            
            # Create a user profile
            profile = Profile()
            profile.user_id = request.user.id
            profile.profile_pics = 'report.png'
            profile.save()

            messages.success(request,'Registration Successfully, Proceed to login')
            print('success')
            return redirect('login' +first_name)
        else:
            messages.error(request,'Registration Fail')    
            print('Bad')
    else:
        form = RegistrationForm()
    context = {
        'form':form
    }    

    return render(request, 'accounts/user/register.html',context)



# User dashboard
@login_required(login_url = 'login')
def dashboard(request):
    user = User.objects.get(id=request.user.id)
    if not request.user:
        return HttpResponse('Only register staff can access this page')
    else:

        reports = Report.objects.filter(user=user).order_by('-date_reported')
        count = Report.objects.filter(user=user).count()
        done_report = Report.objects.filter(user=user,status=1).count()
        in_process_report = Report.objects.filter(user=user,status=0).count()
        ignore_report = Report.objects.filter(user=user,status=2).count()
        
    context = {
        'user':user,
        'reports':reports,
        'count':count,
        'done_report':done_report,
        'in_process_report':in_process_report,
        'ignore_report':ignore_report
        
    }
    return render(request,'accounts/user/dashboard.html',context)


# forgotten password
def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/email/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            # send_email.send()
            # send_email.send()
            print(message)

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'accounts/user/forgotPassword.html')

# reset validate email 
def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('resetPassword')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful, proceed to log in')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/user/resetPassword.html')



@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = User.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password updated successfully.')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('change_password')
    return render(request, 'accounts/user/change_password.html')            