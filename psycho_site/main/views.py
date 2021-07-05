from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import Group, User
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django import forms
import matplotlib.pyplot as plt
from io import StringIO
import numpy as np
from . import psycho_tests
from .models import Test1

def can_i_let_him_in(request):
    return request.user.is_authenticated and not request.user.is_superuser


# def return_graph():
#
#     x = np.arange(0,np.pi*8,.1)
#     y = np.sin(x)
#
#     plt.style.use('seaborn-dark-palette')
#
#     fig = plt.figure(dpi=2000)
#     plt.plot(x,y)
#
#     imgdata = StringIO()
#     fig.savefig(imgdata, format='svg', transparent=True)
#     imgdata.seek(0)
#
#     data = imgdata.getvalue()
#     return data

def home(request):
    if not can_i_let_him_in(request):
        return redirect('login')
    res1 = Test1.objects.all().filter(username=request.user)
    if len(res1) == 0:
        res1 = None
    else:
        res1 = res1[0]
    return render(request, 'home.html', {'cur_page' : 'home', 'res1' : res1})


def account(request):
    if not can_i_let_him_in(request):
        return redirect('login')
    return render(request, 'account.html', {'cur_page' : 'account'})


def statistics(request):
    if not can_i_let_him_in(request):
        return redirect('statistics')
    return render(request, 'statistics.html', {'cur_page' : 'statistics'})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None and not user.is_superuser:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form' : form})


def signout_view(request):
    logout(request)
    return redirect('login')

def change_password(request):
    if not can_i_let_him_in(request):
        return redirect('login')
    messege = None
    request.POST()
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messege = "Ваш пароль был успешно изменен"
        else:
            messege = "Форма смены пароля невалидна"
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form, 'messege' : messege})

def test_first(request):
    if not can_i_let_him_in(request):
        return redirect('login')
    form = forms.Form(request.POST)
    messege = None
    messege2 = None
    array = psycho_tests.test1
    if request.method == 'POST':
        data = form.data
        # messege = data.get("1")
        # messege2 = data.get("2")
        audio = "2, 6, 7, 13, 15, 17, 20, 24, 26, 33, 34, 36, 37, 43, 46, 48".split(',')
        visual = "1, 5, 8, 10, 12, 14, 19, 21, 23, 27, 31, 32, 39, 40, 42, 45".split(',')
        kinest = "3, 4, 9, 11, 16, 18, 22, 25, 28, 29, 30, 35, 38, 41, 44, 47".split(',')

        audio_res = 0
        visual_res = 0
        kinest_res = 0
        for i in audio:
            audio_res += (str(data.get(i.strip())) == 'yes')
        for i in visual:
            visual_res += (str(data.get(i.strip())) == 'yes')
        for i in kinest:
            kinest_res += (str(data.get(i.strip())) == 'yes')
        messege = "audio: " + str(audio_res) + ", visual: " + str(visual_res) + ", kinest: " + str(kinest_res)
        messege2 = 'sasasas'
        res = Test1.objects.all().filter(username=request.user)
        if len(res) == 0:
            Test1.objects.create(username=request.user, audio=audio_res, visual=visual_res, kinest=kinest_res)
        else:
            res = res[0]
            res.audio = audio_res
            res.visual = visual_res
            res.kinest = kinest_res
            res.save()



    return render(request, 'test1.html', {'questions' : array, 'messege' : messege, 'messege2' : messege2, 'res' : len(Test1.objects.all())})