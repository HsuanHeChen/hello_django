from django.shortcuts import render, redirect
from django.contrib import auth, messages


# Create your views here.


def login(request):
    if request.method == 'POST':
        name = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=name, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                messages.add_message(request, messages.SUCCESS, 'Login successfully.')
                return redirect('/')
            else:
                messages.add_message(request, messages.ERROR, 'User not active.')
        else:
            messages.add_message(request, messages.ERROR, 'User not found.')
    return render(request, "login.html", locals())


def logout(request):
    auth.logout(request)
    messages.add_message(request, messages.SUCCESS, 'Logout successfully.')
    return redirect('/')
