from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, UserLoginForm

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('user_login')  # Change 'login' to your login url name
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard_index')  # Change 'dashboard' to your dashboard url name
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form, 'title': 'Login'})
