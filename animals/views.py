from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from livestock import settings
from django.core.mail import EmailMessage, send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import  stock
from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import render
from .forms import UploadFileForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from .forms import ProfileForm
from django.shortcuts import redirect, render, get_object_or_404
from  .models import *


# Create your views here.


def welcome(request):
    if request.method == "POST":
        email = request.POST['email']
        username  = request.POST['username']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('/')

        if password != cpassword:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')

        if email in [None, '']:
            messages.error(request, "Email is required")
            return redirect('signup')

        if username in [None, '']:
            messages.error(request, "Username is required")
            return redirect('signup')

        if password in [None, '']:
            messages.error(request, "Password is required")
            return redirect('signup')

        if cpassword in [None, '']:
            messages.error(request, "Password Confirmation is required")
            return redirect('signup')            

        newuser = User.objects.create_user(username, email, password)
        newuser.save()
        
        return redirect('login/')
    return render(request, "animals/welcome.html")





def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'animals/signup.html', {'form': form})


def login_view(request):
    if request.method == "POST":
      user = request.POST['username']
      request.session['user']=user
      pas = request.POST['password']
      user = authenticate(request, username=user, password=pas)

      if user is not None:
          login(request, user)
          return redirect('/home')
      else:
          messages.error(request, "INVALID CREDENTIALS")
          return redirect('/login')
    return render(request, "animals/login.html")


@login_required(login_url='login')
def home(request):
    data = stock.objects.all()
    context = {"data": data}
    
    return render(request, "animals/home.html", context)


def add(request):
    if request.method == "POST":
        aid = request.POST['aid']
        aclass = request.POST['aclass']
        sex = request.POST['sex']
        weight = request.POST['weight']
        insurance = request.POST['insurance']
        vstatus = request.POST['vstatus']
        vdate = request.POST['vdate']
        ddate = request.POST['ddate']
        newstock = stock(id=aid, aclass=aclass, sex=sex, weight=weight, insurance=insurance, vacstatus=vstatus, vdate=vdate, ddate=ddate)
        newstock.save()
        return redirect('/home')
    return render(request, "animals/add.html")
    

def edit(request, id):
    obj = stock.objects.get(id=id)
    context = {"obj": obj}
    return render(request, "animals/edit.html", context)

def logout_view(request):
    logout(request)
    return redirect('/')

# def delete_view(request, id):
#     obj = stock.objects.get(id=id)
#     obj.delete()
#     data = stock.objects.all()
#     context = {"data": data}
#     return redirect('', context)

def delete_view(request, id):
    obj = get_object_or_404(stock, id=id)
    obj.delete()
    return redirect('home')

@ensure_csrf_cookie
def upload_display_video(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            #print(file.name)
            handle_uploaded_file(file)
            return render(request, "animals/upload_display_video.html", {'filename': file.name})
    else:
        form = UploadFileForm()
        return redirect('/home')
    return render(request, 'animals/upload_display_video.html', {'form': form})

def handle_uploaded_file(f):
    with open(f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


# def profile(request):
#     form =User.objects.filter(username=request.session['user_name'])
#     if request.method == 'POST':
#         form = User.objects.filter(username=request.session['user_name'])
#         if form.is_valid():
#             form.save()
#             return redirect('/home')  # You can change 'profile' to the URL name of your profile view
#     else:
#         form = ProfileForm(instance=request.user.profile)
#     return render(request, 'animals/profile1.html', {'form': form})

from django.contrib.auth.models import User
from .models import Profile

def profile(request):
    userdata = request.session['user']
    try:
        user = User.objects.get(username=userdata)
        try:
            profiles = Profile.objects.get(user=user)
            return render(request, 'animals/profile.html', {'profile': profiles, 'user': user})
        except Profile.DoesNotExist:
            return redirect('/login')
    except User.DoesNotExist:
        return redirect('/login')

