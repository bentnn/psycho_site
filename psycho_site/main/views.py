from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import Group, User
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django import forms
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from . import psycho_tests
from .models import *
from .graphs import *



def can_i_let_him_in(request):
    return request.user.is_authenticated and not request.user.is_superuser


# def return_graph():
#
#     x = np.arange(0, np.pi*8, .1)
#     y = np.sin(x)
#
#     plt.style.use('seaborn-dark-palette')
#
#     fig = plt.figure(dpi=2000)
#     plt.plot(x, y)
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
    res = [None for _ in range(5)]
    res[0] = Test1.objects.all().filter(user=request.user).last()
    res[1] = Test2.objects.all().filter(user=request.user).last()
    res[2] = Test3.objects.all().filter(user=request.user).last()
    res[3] = Test4.objects.all().filter(user=request.user).last()
    res[4] = Test5.objects.all().filter(user=request.user).last()
    return render(request, 'home.html', {'cur_page': 'home', 'res': res,
                                         'graph': return_graph_5_3(Test5.objects.all().filter(user=request.user))})


def account(request):
    if not can_i_let_him_in(request):
        return redirect('login')
    return render(request, 'account.html', {'cur_page': 'account'})


def statistics(request):
    if not can_i_let_him_in(request):
        return redirect('statistics')
    tests = [Test1.objects.all().filter(user=request.user),
             Test2.objects.all().filter(user=request.user),
             Test3.objects.all().filter(user=request.user),
             Test4.objects.all().filter(user=request.user),
             Test5.objects.all().filter(user=request.user)]
    graph1 = [return_graph1_1(tests[0]), return_graph1_2(tests[0])]
    graph2 = [return_graph2_1(tests[1]), return_graph2_2(tests[1])]
    graph3 = return_graph3(tests[2])
    graph4 = [return_graph4_1(tests[3]), return_graph4_2(tests[3])]
    graph5 = [return_graph_5_1(tests[4]), return_graph_5_2(tests[4]), return_graph_5_3(tests[4])]
    return render(request, 'statistics.html', {'cur_page': 'statistics', 'tests': tests, 'graph1': graph1,
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


def change_password(request):
    if not can_i_let_him_in(request):
        return redirect('login')
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


def change_info(request):
    if not can_i_let_him_in(request):
        return redirect('login')
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email
        request.user.save()
        return redirect('account')

    return render(request, 'change_info.html')


def send_mail(user, new):
    addr_from = "hse.tests@yandex.ru"
    password = "ihoqgelsccaxmyha"
    # addr_from = "anticovidbracelet@yandex.com"
    # password  = "bisxbtrjucwaebfi"

    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = user.email
    msg['Subject'] = 'Информация смене пароля'

    text = "Здравствуйте"
    if user.first_name != "":
        text += ", " + user.first_name
    text += ". На сайте психологических тестов от высшей школы экономики была активирована функция " \
            "'восстановить пароль' для вашего аккаунта."
    text += "\nВаш новый пароль: " + new + ". Вы сможете заменить его в вашем личном кабинете."
    msg.attach(MIMEText(text, 'plain'))
    try:
        print("0")
        server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
        print("01")
        server.login(addr_from, password)
        print("1")
        server.sendmail(addr_from, user.email, msg.as_string())
        print("2")
        server.quit()
        return 0
    except:
        return 1


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


def test_first(request):
    if not can_i_let_him_in(request):
        return redirect('login')
    message = None
    array = psycho_tests.test1
    if request.method == 'POST':
        data = forms.Form(request.POST).data
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
        message = "Аудиальный канал восприятия: " + str(audio_res) + ", Визуальный канал восприятия: "\
                  + str(visual_res) + ", Кинестетический канал восприятия: " + str(kinest_res)
        Test1.objects.create(user=request.user, audio=audio_res, visual=visual_res, kinest=kinest_res)

    return render(request, 'test1.html', {'questions': array, 'message': message})


def test_second(request):
    if not can_i_let_him_in(request):
        return redirect('login')
    message = None
    array = psycho_tests.test2
    if request.method == 'POST':
        data = forms.Form(request.POST).data
        rt = [3, 4, 6, 7, 9, 12, 13, 14, 17, 18]
        lt = [22, 23, 24, 25, 28, 29, 31, 32, 34, 35, 37, 38, 40]
        rt_res = 35
        for i in range(1, 21):
            pos = str(i)
            res = int(data.get(pos))
            if i in rt:
                rt_res += res
            else:
                rt_res -= res
        lt_res = 35
        for i in range(21, 41):
            pos = str(i)
            res = int(data.get(pos))
            if i in lt:
                lt_res += res
            else:
                lt_res -= res

        Test2.objects.create(user=request.user, rt=rt_res, lt=lt_res)
        if rt_res <= 30:
            message = "низкая реактивная тревожность"
        elif 31 <= rt_res <= 45:
            message = "умеренная реактивная тревожность"
        else:
            message = "высокая реактивная тревожность"
        if lt_res <= 30:
            message += ", низкая личностная тревожность"
        elif 31 <= lt_res <= 45:
            message += ", умеренная личностная тревожность"
        else:
            message += ", высокая личностная тревожность"
    return render(request, 'test2.html', {'questions': array, 'message': message})


def test_third(request):
    if not can_i_let_him_in(request):
        return redirect('login')
    message = None
    array = psycho_tests.test3
    if request.method == 'POST':
        data = forms.Form(request.POST).data
        ud = [1, 3, 4, 7, 8, 9, 10, 13, 15, 19]
        ud_res = 0
        for i in range(1, 21):
            pos = str(i)
            res = int(data.get(pos))
            if i in ud:
                ud_res += res
            else:
                ud_res += 5 - res
        Test3.objects.create(user=request.user, ud=ud_res)
        if ud_res <= 50:
            message = "У вас отсутствует депрессия"
        elif 51 <= ud_res <= 60:
            message = "У вас легкая депрессия ситуативного или невротического генеза"
        elif 61 <= ud_res <= 70:
            message = "У вас субдепрессивное состояние или маскированная депрессия"
        else:
            message = "У вас истинное депрессивное состояние"
    return render(request, 'test3.html', {'questions': array, 'message': message})


def test_fourth(request):
    if not can_i_let_him_in(request):
        return redirect('login')
    message = None
    array = psycho_tests.test4
    if request.method == 'POST':
        data = forms.Form(request.POST).data
        being_q = [1, 2, 7, 8, 13, 14, 19, 20, 25, 26]
        activity_q = [3, 4, 9, 10, 15, 16, 21, 22, 27, 28]
        mood_q = [5, 6, 11, 12, 17, 18, 23, 24, 29, 30]
        inverse_q = [1, 2, 5, 6, 7, 8, 11, 12, 14, 17, 18, 19, 20,
                     23, 24, 25, 26, 29, 30]
        being_res = 0
        activity_res = 0
        mood_res = 0
        for i in being_q:
            pos = str(i)
            res = int(data.get(pos))
            if i in inverse_q:
                being_res += 8 - res
            else:
                being_res += res
        being_res /= len(being_q)
        for i in activity_q:
            pos = str(i)
            res = int(data.get(pos))
            if i in inverse_q:
                activity_res += 8 - res
            else:
                activity_res += res
        activity_res /= len(activity_q)
        for i in mood_q:
            pos = str(i)
            res = int(data.get(pos))
            if i in inverse_q:
                mood_res += 8 - res
            else:
                mood_res += res
        mood_res /= len(mood_q)
        Test4.objects.create(user=request.user, activity=activity_res, being=being_res, mood=mood_res)
        message = ['', '']
        message[0] = "Активность = " + str(activity_res) + "/7, самочувствие = " + str(being_res) + \
                     "/7, настроение = " + str(mood_res) + "/7."
        sum = activity_res + being_res + mood_res
        a_proc = activity_res / sum * 100
        b_proc = being_res / sum * 100
        m_proc = 100 - b_proc - a_proc
        message[1] = "В процентном соотношении: активность - {:.2f}%, самочувствие - " \
                     "{:.2f}%, настроение - {:.2f}%".format(a_proc, b_proc, m_proc)
    return render(request, 'test4.html', {'questions': array, 'message': message})


def test_fifth(request):
    if not can_i_let_him_in(request):
        return redirect('login')
    message = None
    array = psycho_tests.test5
    if request.method == 'POST':
        data = forms.Form(request.POST).data
        sinc_q_yes = [6, 24, 36]
        sinc_q_no = [12, 18, 30, 42, 48, 54]
        extrav_q_yes = [1, 3, 8, 10, 13, 17, 22, 27, 39, 44, 46, 49, 53, 56]
        extrav_q_no = [5, 15, 20, 29, 32, 34, 37, 41, 51]
        neuro_q = [2, 4, 7, 9, 11, 14, 16, 19, 21, 23, 26, 28, 31, 33, 35, 38, 40, 43, 45, 47, 50, 52, 55, 57]
        sinc_res = 0
        extrav_res = 0
        neuro_res = 0
        for i in sinc_q_yes:
            sinc_res += (str(data.get(str(i))) == 'yes')
        for i in sinc_q_no:
            sinc_res += (str(data.get(str(i))) == 'no')
        for i in extrav_q_yes:
            extrav_res += (str(data.get(str(i))) == 'yes')
        for i in extrav_q_no:
            extrav_res += (str(data.get(str(i))) == 'no')
        for i in neuro_q:
            neuro_res += (str(data.get(str(i))) == 'yes')
        Test5.objects.create(user=request.user, sincerity=sinc_res, extrav=extrav_res, neuro=neuro_res)
        message = ['', '', '']
        message[0] = "Показатель искренности - " + str(sinc_res) + " из 9, что свидетельствует о"
        if sinc_res <= 3:
            message[0] += "б откровенности"
        elif 4 <= sinc_res <= 6:
            message[0] += " ситуативности"
        else:
            message[0] += " лживости"
        message[1] = "Показатель экстравертности - " + str(extrav_res) + " из 24. Это означает, что вы "
        if extrav_res <= 2:
            message[1] += "сверхинтроверт"
        elif 3 <= extrav_res <= 6:
            message[1] += "интроверт"
        elif 7 <= extrav_res <= 10:
            message[1] += "потенциальный интроверт"
        elif 11 <= extrav_res <= 14:
            message[1] += "амбиверт"
        elif 15 <= extrav_res <= 18:
            message[1] += "потенциальный экстраверт"
        elif 19 <= extrav_res <= 22:
            message[1] += "экстраверт"
        else:
            message[1] += "сверхэкстраверт"
        message[2] = "Показатель невротизма - " + str(neuro_res) + " из 24. Это означает, что вы "
        if neuro_res <= 2:
            message[2] += "сверхконкордант"
        elif 3 <= neuro_res <= 6:
            message[2] += "конкордант"
        elif 7 <= neuro_res <= 10:
            message[2] += "потенциальный конкордант"
        elif 11 <= neuro_res <= 14:
            message[2] += "нормостеник"
        elif 15 <= neuro_res <= 18:
            message[2] += "потенциальный дискордант"
        elif 19 <= neuro_res <= 22:
            message[2] += "дискордант"
        else:
            message[2] += "сверхдискордант"
    return render(request, 'test5.html', {'questions': array, 'message': message})
