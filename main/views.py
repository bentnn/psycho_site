from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import Group, User
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django import forms
from .psycho_tests import about_tests
from .models import *
from rest.models import UserTelegramID
from rest.views import get_user_telegram
from .graphs import *
from .mail_sendler import send_mail
from .test_counters import *
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from .test_answers import *
from .test_counters import *


@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')


@login_required(login_url='login')
def tests(request):
    return render(request, 'tests.html', {'tests': about_tests})


@login_required(login_url='login')
def account(request):
    user_telegram_id = get_user_telegram(user=request.user)
    user_telegram_id = user_telegram_id.telegram_id if user_telegram_id else None
    return render(request, 'account.html', {'cur_page': 'account', 'telegram_id': user_telegram_id})


@login_required(login_url='login')
def statistics(request):
    tests = [Test1.objects.all().filter(user=request.user),
             Test2.objects.all().filter(user=request.user),
             Test3.objects.all().filter(user=request.user),
             Test4.objects.all().filter(user=request.user),
             Test5.objects.all().filter(user=request.user)]
    graph1 = None
    graph2 = None
    graph3 = None
    graph4 = None
    graph5 = None
    if tests[0]:
        graph1 = [lines_graph(tests[0]), pie_graph(tests[0])]
    if tests[1]:
        graph2 = [fill_line_graph(tests[1], 'rt', [30, 45]), fill_line_graph(tests[1], 'lt')]
    if tests[2]:
        graph3 = return_graph3(tests[2])
    if tests[3]:
        graph4 = [return_graph4_1(tests[3]), return_graph4_2(tests[3])]
    if tests[4]:
        graph5 = [return_graph_5_1(tests[4]), return_graph_5_2(tests[4]), return_graph_5_3(tests[4])]
    return render(request, 'statistics.html', {'tests': tests, 'graph1': graph1,
                                               'graph2': graph2, 'graph3': graph3, 'graph4': graph4, 'graph5': graph5})


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
    return render(request, 'login.html', {'form': form})


def check_in_view(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'check_in.html', {'form': form})


def signout_view(request):
    logout(request)
    return redirect('login')


def forgot_password(request):
    message = None
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        user = User.objects.all().filter(username=username, email=email)
        if len(user) != 0:
            password = User.objects.make_random_password()
            user[0].set_password(password)
            user[0].save()
            res = send_mail(user[0], password)
            message = "На указанный вами адрес отправлен новый пароль" + str(res)
        else:
            message = "Пользователь не найден"

    return render(request, 'forgot_password.html', {'message': message})


@login_required(login_url='login')
def change_password(request):
    message = None
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            message = "Ваш пароль был успешно изменен"
        else:
            message = "Форма смены пароля невалидна"
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form, 'message': message})


@login_required(login_url='login')
def change_info(request):
    user_telegram = get_user_telegram(user=request.user)
    user_telegram_id = user_telegram.telegram_id if user_telegram else None

    if request.method == 'POST':
        telegram_id = request.POST.get('telegram_id')
        if telegram_id:
            telegram_id = int(telegram_id)
            if user_telegram_id != telegram_id and UserTelegramID.objects.filter(telegram_id=telegram_id).exists():
                return render(request, 'change_info.html',
                              {'telegram_id': user_telegram_id,
                               'message': f'Telegram ID "{telegram_id}" уже привязан к другому аккаунту на сайте. '
                                          f'Отвяжите его перед привязкой к этому. '
                                          f'Если ID привязан к аккаунту, к которому у вас нет доступа, '
                                          f'вы можете отвязать его в telegram боте через пользователя с этим ID.'})
            if user_telegram:
                user_telegram.telegram_id = telegram_id
                user_telegram.save()
            else:
                UserTelegramID.objects.create(user=request.user, telegram_id=telegram_id)
        elif user_telegram:
            user_telegram.delete()
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email
        request.user.save()
        return redirect('account')
    return render(request, 'change_info.html', {'telegram_id': user_telegram_id})


@login_required(login_url='login')
def test1(request):
    message = None
    if request.method == 'POST':
        data = forms.Form(request.POST).data
        message = count_test1(data, request.user, via_telegram=False)
    return render(request, 'test_page.html',
                  {'test': about_tests['test1'], 'message': message})


@login_required(login_url='login')
def test2(request):
    message = None
    if request.method == 'POST':
        data = forms.Form(request.POST).data
        message = count_test2(data, request.user, via_telegram=False)

    return render(request, 'test_page.html',
                  {'test': about_tests['test2'], 'message': message})


@login_required(login_url='login')
def test3(request):
    message = None
    if request.method == 'POST':
        data = forms.Form(request.POST).data
        message = count_test3(data, request.user, via_telegram=False)

    return render(request, 'test_page.html',
                  {'test': about_tests['test3'], 'message': message})


@login_required(login_url='login')
def test4(request):
    message = None
    if request.method == 'POST':
        data = forms.Form(request.POST).data
        message = count_test4(data, request.user, via_telegram=False)
    return render(request, 'test_page.html',
                  {'test': about_tests['test4'], 'message': message})


@login_required(login_url='login')
def test5(request):
    message = None
    if request.method == 'POST':
        data = forms.Form(request.POST).data
        message = count_test5(data, request.user, via_telegram=False)
    return render(request, 'test_page.html',
                  {'test': about_tests['test5'], 'message': message})


@login_required(login_url='login')
def test6(request):
    message = None
    if request.method == 'POST':
        data = forms.Form(request.POST).data
        message = count_test6(data, request.user, via_telegram=False)
    return render(request, 'test_page.html',
                  {'test': about_tests['test6'], 'message': message})


@login_required(login_url='login')
def test7(request):
    message = None
    if request.method == 'POST':
        data = forms.Form(request.POST).data
        message = count_test7(data, request.user, via_telegram=False)
    return render(request, 'test_page.html',
                  {'test': about_tests['test7'], 'message': message})


@login_required(login_url='login')
def test8(request):
    message = None
    if request.method == 'POST':
        data = forms.Form(request.POST).data
        message = count_test8(data, request.user, via_telegram=False)

    return render(request, 'test_page.html',
                  {'test': about_tests['test8'], 'message': message})


@login_required(login_url='login')
def test9(request):
    message = None
    if request.method == 'POST':
        data = forms.Form(request.POST).data
        message = count_test9(data, request.user, via_telegram=False)

    return render(request, 'test_page.html',
                  {'test': about_tests['test9'], 'message': message})


@login_required(login_url='login')
def test10(request):
    message = None
    if request.method == 'POST':
        data = forms.Form(request.POST).data
        message = count_test10(data, request.user, via_telegram=False)

    return render(request, 'test_page.html',
                  {'test': about_tests['test10'], 'message': message})


@login_required(login_url='login')
def test11(request):
    message = None
    if request.method == 'POST':
        data = forms.Form(request.POST).data
        message = count_test11(data, request.user, via_telegram=False)

    return render(request, 'test_page.html',
                  {'test': about_tests['test11'], 'message': message})


@login_required(login_url='login')
def test12(request):
    message = None
    if request.method == 'POST':
        data = forms.Form(request.POST).data
        message = count_test12(data, request.user, via_telegram=False)

    return render(request, 'test_page.html',
                  {'test': about_tests['test12'], 'message': message})


@login_required(login_url='login')
def test13(request):
    message = None
    if request.method == 'POST':
        data = forms.Form(request.POST).data
        message = count_test13(data, request.user, via_telegram=False)
    return render(request, 'test_page.html',
                  {'test': about_tests['test13'], 'message': message})


@login_required(login_url='login')
def staffroom(request):
    if not request.user.is_staff:
        return redirect('home')
    return render(request, 'staffroom.html', {'cur_page': 'staffroom'})


# Получение спика электронных адресов пользователей.
# Сделано для участия в студенческом конкурсе проектов.
@login_required(login_url='login')
def download_emails(request):
    if not request.user.is_staff:
        return redirect('home')

    users = list(filter(lambda user: user.email, User.objects.all().filter(is_superuser=False, is_staff=False)))
    group1 = users[:int(len(users) / 2)]
    group2 = users[len(group1):]
    emails1 = ", ".join([user.email for user in group1])
    emails2 = ", ".join([user.email for user in group2])
    usernames1 = ", ".join([user.username for user in group1])
    usernames2 = ", ".join([user.username for user in group2])

    file_to_send = ContentFile(f"Всего участников эксперимента: {len(users)}\n\n"
                               f"Группа 1(колличество: {len(group1)}):\n" + usernames1 +
                               "\nЭлектронные почты:\n" + emails1 +
                               f"\n\nГруппа 2(колличество: {len(group2)}):\n" + usernames2 +
                               "\nЭлектронные почты:\n" + emails2)
    response = HttpResponse(file_to_send, 'text/plain')
    response['Content-Disposition'] = 'attachment; filename="experiment.txt"'
    return response
