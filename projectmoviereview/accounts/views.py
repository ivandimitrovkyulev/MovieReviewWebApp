from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    login,
    logout,
    authenticate,
)

from .forms import UserCreateForm


def signupaccount(request):

    if request.method == "GET":
        return render(request, 'signupaccount.html', {'form': UserCreateForm})

    else:
        user_name = request.POST['username']
        pass_1 = request.POST['password1']
        pass_2 = request.POST['password2']

        if pass_1 == pass_2:
            try:
                user = User.objects.create_user(user_name, password=pass_1)
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signupaccount.html',
                              {'form': UserCreateForm,
                               'error': 'Username unavailable. Choose different username.'})

        else:
            return render(request, 'signupaccount.html',
                          {'form': UserCreateForm,
                           'error': 'Passwords do not match'})


@login_required
def logoutaccount(request):
    logout(request)
    return redirect('home')


def loginaccount(request):
    if request.method == 'GET':
        return render(request, 'loginaccount.html', {'form': AuthenticationForm})

    else:
        user_name = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=user_name, password=password)

        if user is None:
            return render(request, 'loginaccount.html',
                          {'form': AuthenticationForm,
                           'error': 'username and password do not match'})

        else:
            login(request, user)
            return redirect('home')
