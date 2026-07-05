from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm

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

@login_required
def user_logout(request):
    logout(request)
    return redirect('')
