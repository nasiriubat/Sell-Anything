from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView, CreateView, UpdateView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from Core.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserUpdateForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
import random
import string

def randomString(stringlength=6):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringlength))

code = randomString()


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        password2 = request.POST['password2']
        user = User

        context ={
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'username': username,
            'phone': phone,
            'password': password,
        }

        if password == password2:
            if user.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken')
                return redirect('register')
            else:
                if user.objects.filter(email=email).exists():
                    messages.error(request, 'Email is already used')
                    return redirect('register')
                else:
                    if user.objects.filter(phone=phone).exists():
                        messages.error(request, 'Phone no  is already used')
                        return redirect('register')
                    else:
                        send_mail(
                            'Account Creation Confirmation',
                            'Hi '+ first_name + 'You Confirmation code is: ' +code,
                            'shuvo131662@gmail.com',
                            [email],
                            fail_silently=False
                        )
                        request.method = 'GET'
                        return render(request, 'registration/confirmregister.html', context)
        else:
            messages.error(request,'passwords do not match')
            return redirect('register')
    else:
        return render(request, 'registration/register.html')

def confirmregister(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirmcode = request.POST['confirmcode']
        user = User
        context ={
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'username': username,
            'phone': phone,
            'password': password,
        }
        if code == confirmcode:
            user = user.objects.create_user(username=username, password=password, email=email, phone=phone, first_name=first_name, last_name=last_name)
            user.save()
            login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('home')
        else:
            messages.error(request, 'Invalid Confirmation Code')
            return render(request, 'registration/confirmregister.html', context)
    else:
        return redirect('register')

@login_required
def userlogout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def userlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request, 'registration/login.html')






@login_required
def profile(request):
    if request.method == 'POST':
        form=UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been updated")
            return redirect('profile')
        
    else:
        form=UserUpdateForm(instance=request.user)

    context={'u_form':form}
    return render(request,'registration/profile.html',context)

