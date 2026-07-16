from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LogInForm

def user_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("courses:list")
    else:
        form = SignUpForm()
    return render(request, 'users/user_signup.html', { 'form': form })

def user_login(request):
    if request.method == "POST":
        form = LogInForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('courses:list')
            else:
                messages.error(request, "INVALID")
    else:
        form = LogInForm()
    return render(request, "users/user_login.html", { 'form': form })

@login_required
def user_logout(request):
    logout(request)
    return redirect('marketplace:course_public_list')
