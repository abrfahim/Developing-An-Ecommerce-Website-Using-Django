from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

# Authentication
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate


# Forms & Model
from AppLogin.models import Profile
from AppLogin.forms import ProfileForm, SignupForm

# Messages
from django.contrib import messages


# Create your views here.

def sign_up (request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Created Successfully!')
            return HttpResponseRedirect(reverse('AppLogin:log_in'))
    
    diction = {'form': form, 'titles': 'Create an Account'}
    return render(request, 'AppLogin/signup.html',context=diction)


def log_in(request):
    
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You are logged in successfully!')
                return HttpResponseRedirect(reverse('AppShop:homepage'))
            
    diction = {'form': form}
    return render(request, 'AppLogin/login.html' , context=diction)


@login_required
def log_out(request):
    logout(request)
    messages.info(request, 'Your are logged out!')
    return HttpResponseRedirect(reverse('AppShop:homepage'))    


@login_required
def user_profile(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Saved!')
            form = ProfileForm(instance=profile)
    diction = {'form': form}
    return render(request, 'AppLogin/user_profile.html', context=diction)