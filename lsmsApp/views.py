from django.shortcuts import render, redirect
from lsmsApp.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from lsmsApp import models, forms
from django.http import HttpResponse
import json

def BASE(request):
    return render(request, 'base.html')
def LOGIN(request):
    return render(request, 'login.html')

def dologin(request):
    
    if request.method == 'POST':
        user = EmailBackEnd.authenticate(request,
        username = request.POST.get('email'), password=request.POST.get('password'))

        if user!=None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('hod_home')
            elif user_type == '2':
                return redirect('employee_home')
            else:
                messages.error(request, 'Email and Password Are Invalid')    
                return redirect('login') 
        else:
            messages.error(request, 'Email and Password Are Invalid')    
            return redirect('login') 
         

def dologout(request):
    logout(request)
    return redirect('login')


def PROFILE(request):
    
    user = models.CustomUser.objects.get(id=1)
    context = {
        'user': user,
    }
    return render(request, 'profile.html', context)

def PROFILE_UPDATE(request):
    if request.method == 'POST':
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        #email = request.POST.get('email')
        #username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            customuser = models.CustomUser.objects.get(id=request.user.id)

            customuser.first_name = first_name
            customuser.last_name = last_name
           
            if password != None and password != "":
                customuser.set_password(password)
           
            customuser.save()
            messages.success(request, 'Your Profile Updated Successfully !')
            return redirect('profile')    
        except:
            messages.error(request, 'Failed To Update Your Profile')
            

    return render(request, 'profile.html') 