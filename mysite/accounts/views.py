import sys
from accounts.models import Token, ListUser
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import messages
from django.shortcuts import redirect, render
# from django.core.mail import send_mail


def account_login(request):
    if request.method == 'GET':
        return render(request, 'accounts/login.html')
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            token = Token.objects.create(email=email)
            # TODO - send_email
            # send_mail(
            #     'Your login code for superlists',
            #     'Use this code to log in: {uid}\n'.format(uid=token.uid),
            #     'noreply@superlists',
            #     [email],
            # )
            # messages.success(request, 'Email sent to {}.'.format(email))
            messages.success(request, token.uid)
            return redirect('/accounts/login')

        try:
            token = Token.objects.get(uid=request.POST.get('uid').strip())
            user = ListUser.objects.get(email=token.email)
        except Token.DoesNotExist:
            user = None
        except ListUser.DoesNotExist:
            user = ListUser.objects.create(email=token.email)

        if user:
            auth_login(request, user)
            messages.success(request, 'Logged in as {}'.format(user.email))
            return redirect('/lists/')

        messages.error(request, 'Invalid token')
        return redirect('/accounts/login')


def account_logout(request):
    auth_logout(request)
    return redirect('/lists/')
