from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import Group, User
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django import forms
from .psycho_tests import about_tests
from .models import *
from .graphs import *
from .mail_sendler import send_mail
from .test_counters import *
import datetime
import pytz
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from .test_answers import *


@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')


@login_required(login_url='login')
def tests(request):
    return render(request, 'tests.html', {'tests': about_tests})


@login_required(login_url='login')
def account(request):
    return render(request, 'account.html', {'cur_page': 'account'})


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
            message = "???? ?????????????????? ???????? ?????????? ?????????????????? ?????????? ????????????" + str(res)
        else:
            message = "???????????????????????? ???? ????????????"

    return render(request, 'forgot_password.html', {'message': message})


@login_required(login_url='login')
def change_password(request):
    message = None
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            message = "?????? ???????????? ?????? ?????????????? ??????????????"
        else:
            message = "?????????? ?????????? ???????????? ??????????????????"
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form, 'message': message})


@login_required(login_url='login')
def change_info(request):
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


@login_required(login_url='login')
def test1(request):
    message = None
    if request.method == 'POST':
        data = forms.Form(request.POST).data
        audio = [2, 6, 7, 13, 15, 17, 20, 24, 26, 33, 34, 36, 37, 43, 46, 48]
        visual = [1, 5, 8, 10, 12, 14, 19, 21, 23, 27, 31, 32, 39, 40, 42, 45]
        kinest = [3, 4, 9, 11, 16, 18, 22, 25, 28, 29, 30, 35, 38, 41, 44, 47]

        counter = lambda array: sum(str(data.get(str(i))) == 'yes' for i in array)
        audio_res = counter(audio)
        visual_res = counter(visual)
        kinest_res = counter(kinest)
        message = f"???????????????????? ?????????? ????????????????????: {audio_res}, " \
                  f"???????????????????? ?????????? ????????????????????: {visual_res}, " \
                  f"?????????????????????????????? ?????????? ????????????????????: {kinest_res}"
        Test1.objects.create(user=request.user, audio=audio_res, visual=visual_res, kinest=kinest_res)
    return render(request, 'test_page.html',
                  {'test': about_tests['test1'], 'message': message})


@login_required(login_url='login')
def test2(request):
    message = None
    if request.method == 'POST':
        data = forms.Form(request.POST).data
        rt = [3, 4, 6, 7, 9, 12, 13, 14, 17, 18]
        lt = [22, 23, 24, 25, 28, 29, 31, 32, 34, 35, 37, 38, 40]

        rt_res = 35 + sum(int(data.get(str(i))) if i in rt
                          else -int(data.get(str(i)))
                          for i in range(1, 21))
        lt_res = 35 + sum(int(data.get(str(i))) if i in lt
                          else -int(data.get(str(i)))
                          for i in range(21, 41))
        Test2.objects.create(user=request.user, rt=rt_res, lt=lt_res)

        if rt_res <= 30:
            message = "???????????? ???????????????????? ??????????????????????"
        elif 31 <= rt_res <= 45:
            message = "?????????????????? ???????????????????? ??????????????????????"
        else:
            message = "?????????????? ???????????????????? ??????????????????????"
        if lt_res <= 30:
            message += ", ???????????? ???????????????????? ??????????????????????"
        elif 31 <= lt_res <= 45:
            message += ", ?????????????????? ???????????????????? ??????????????????????"
        else:
            message += ", ?????????????? ???????????????????? ??????????????????????"
    return render(request, 'test_page.html',
                  {'test': about_tests['test2'], 'message': message})


@login_required(login_url='login')
def test3(request):
    message = None
    if request.method == 'POST':
        data = forms.Form(request.POST).data
        ud = [1, 3, 4, 7, 8, 9, 10, 13, 15, 19]
        ud_res = sum(int(data.get(str(i))) if i in ud
                     else 5 - int(data.get(str(i)))
                     for i in range(1, 21))
        Test3.objects.create(user=request.user, ud=ud_res)
        if ud_res <= 50:
            message = "?? ?????? ?????????????????????? ??????????????????"
        elif 51 <= ud_res <= 60:
            message = "?? ?????? ???????????? ?????????????????? ???????????????????????? ?????? ???????????????????????????? ????????????"
        elif 61 <= ud_res <= 70:
            message = "?? ?????? ?????????????????????????????? ?????????????????? ?????? ?????????????????????????? ??????????????????"
        else:
            message = "?? ?????? ???????????????? ???????????????????????? ??????????????????"
    return render(request, 'test_page.html',
                  {'test': about_tests['test3'], 'message': message})


@login_required(login_url='login')
def test4(request):
    message = None
    if request.method == 'POST':
        data = forms.Form(request.POST).data

        being_q = [1, 2, 7, 8, 13, 14, 19, 20, 25, 26]
        activity_q = [3, 4, 9, 10, 15, 16, 21, 22, 27, 28]
        mood_q = [5, 6, 11, 12, 17, 18, 23, 24, 29, 30]
        inverse_q = [1, 2, 5, 6, 7, 8, 11, 12, 14, 17, 18, 19, 20,
                     23, 24, 25, 26, 29, 30]

        counter = lambda questions: \
            sum(int(data.get(str(i))) if i in inverse_q
                else 8 - int(data.get(str(i)))
                for i in questions) / len(questions)

        being_res = counter(being_q)
        activity_res = counter(activity_q)
        mood_res = counter(mood_q)

        Test4.objects.create(user=request.user, activity=activity_res, being=being_res, mood=mood_res)
        sum_of_res = activity_res + being_res + mood_res
        a_proc = activity_res / sum_of_res * 100
        b_proc = being_res / sum_of_res * 100
        m_proc = 100 - b_proc - a_proc
        message = "???????????????????? = {}/7, " \
                  "???????????????????????? = {}/7, " \
                  "???????????????????? = {}/7. " \
                  "?? ???????????????????? ??????????????????????: ???????????????????? - {:.2f}%, " \
                  "???????????????????????? - {:.2f}%, " \
                  "???????????????????? - {:.2f}%". \
            format(activity_res, being_res, mood_res, a_proc, b_proc, m_proc)
    return render(request, 'test_page.html',
                  {'test': about_tests['test4'], 'message': message})


@login_required(login_url='login')
def test5(request):
    message = None
    if request.method == 'POST':
        data = forms.Form(request.POST).data
        sinc_q_yes = [6, 24, 36]
        sinc_q_no = [12, 18, 30, 42, 48, 54]
        extrav_q_yes = [1, 3, 8, 10, 13, 17, 22, 27, 39, 44, 46, 49, 53, 56]
        extrav_q_no = [5, 15, 20, 29, 32, 34, 37, 41, 51]
        neuro_q = [2, 4, 7, 9, 11, 14, 16, 19, 21, 23, 26, 28, 31, 33, 35, 38, 40, 43, 45, 47, 50, 52, 55, 57]

        counter = lambda array, value: \
            sum(str(data.get(str(i))) == value for i in array)

        sinc_res = counter(sinc_q_yes, 'yes') + counter(sinc_q_no, 'no')
        extrav_res = counter(extrav_q_yes, 'yes') + counter(extrav_q_no, 'no')
        neuro_res = counter(neuro_q, 'yes')

        Test5.objects.create(user=request.user, sincerity=sinc_res, extrav=extrav_res, neuro=neuro_res)

        message = ['', '', '']
        message[0] = "???????????????????? ?????????????????????? - " + str(sinc_res) + " ???? 9, ?????? ?????????????????????????????? ??"
        if sinc_res <= 3:
            message[0] += "?? ??????????????????????????"
        elif 4 <= sinc_res <= 6:
            message[0] += " ??????????????????????????"
        else:
            message[0] += " ????????????????"
        message[1] = "???????????????????? ?????????????????????????????? - " + str(extrav_res) + " ???? 24. ?????? ????????????????, ?????? ???? "
        if extrav_res <= 2:
            message[1] += "????????????????????????????"
        elif 3 <= extrav_res <= 6:
            message[1] += "??????????????????"
        elif 7 <= extrav_res <= 10:
            message[1] += "?????????????????????????? ??????????????????"
        elif 11 <= extrav_res <= 14:
            message[1] += "????????????????"
        elif 15 <= extrav_res <= 18:
            message[1] += "?????????????????????????? ????????????????????"
        elif 19 <= extrav_res <= 22:
            message[1] += "????????????????????"
        else:
            message[1] += "??????????????????????????????"
        message[2] = "???????????????????? ???????????????????? - " + str(neuro_res) + " ???? 24. ?????? ????????????????, ?????? ???? "
        if neuro_res <= 2:
            message[2] += "??????????????????????????????"
        elif 3 <= neuro_res <= 6:
            message[2] += "????????????????????"
        elif 7 <= neuro_res <= 10:
            message[2] += "?????????????????????????? ????????????????????"
        elif 11 <= neuro_res <= 14:
            message[2] += "??????????????????????"
        elif 15 <= neuro_res <= 18:
            message[2] += "?????????????????????????? ????????????????????"
        elif 19 <= neuro_res <= 22:
            message[2] += "????????????????????"
        else:
            message[2] += "??????????????????????????????"
    return render(request, 'test_page.html',
                  {'test': about_tests['test5'], 'message': '. '.join(message)})


@login_required(login_url='login')
def test6(request):
    message = None
    if request.method == 'POST':
        data = forms.Form(request.POST).data
        positive_effect = sum(int(data[str(i)]) for i in [1, 3, 5, 9, 10, 12, 14, 16, 17, 19])
        negative_effect = sum(int(data[str(i)]) for i in [2, 4, 6, 7, 8, 11, 13, 15, 18, 20])

        message = '?? ??????:\n'
        message += count_message_test6(positive_effect, 22, 39, '??????????????????????')
        message += count_message_test6(negative_effect, 15, 32, '??????????????????????')
        message += '\n?????????????? ?????????????? ?????????????????????? ?????????????? ??? ?????????????????? ???????????????? ??????????????????????????, ' \
                   '?????????????? ???????????????????????? ?? ???????????? ????????????????????????. ???????????? ?????????????? - ?????????????????? ???????????? ?? ??????????????.\n\n' \
                   '?????????????? ?????????????? ?????????????????????? ?????????????? ??? ?????????????????? ?????????????????????? ?????????????????????????? ??????????????????, ' \
                   '???????????????????? ?????????????????????????? (?????????????????? ???? ???????????????????? ??? ?????? ?????????? ???????? ????????, ????????????????????, ??????????????????, ' \
                   '????????, ??????????, ??????????????????????????????????). ???????????? ?????????????? - ?????????????????? ?????????????????????? ?? ??????????????????????????.'
        Test6.objects.create(user=request.user, positive_effect=positive_effect,
                             negative_effect=negative_effect)
    return render(request, 'test_page.html',
                  {'test': about_tests['test6'], 'message': message})


@login_required(login_url='login')
def test7(request):
    message = None
    if request.method == 'POST':
        data = forms.Form(request.POST).data

        counter = lambda array: sum(int(data[str(i)]) for i in array)
        depression = counter([3, 5, 10, 13, 16, 17, 21])
        anxiety = counter([2, 4, 7, 9, 15, 19, 20])
        stress = counter([1, 6, 8, 11, 12, 14, 18])
        message = ''
        for name, answers, number in zip(
            ['?????????? ??????????????????', '?????????? ??????????????', '?????????? ??????????????'],
            [depression_answers, anxiety_answers, stress_asnwers],
            [depression, anxiety, stress]
        ):
            message += f"{name}:\n"
            message += next(ans for scale, ans in answers.items() if number <= scale)
            message += '\n'
        Test7.objects.create(user=request.user, depression=depression,
                             anxiety=anxiety, stress=stress)
    return render(request, 'test_page.html',
                  {'test': about_tests['test7'], 'message': message})


@login_required(login_url='login')
def test8(request):
    message = None
    if request.method == 'POST':
        data = forms.Form(request.POST).data
        self_rating = sum(int(data[str(i)]) for i in [1, 3, 4, 7, 10]) + \
                 sum(3 - int(data[str(i)]) for i in [2, 5, 6, 8, 9])
        message = '???????? ???????????????????? ???? ???????????? ????????????:\n'
        if self_rating <= 15:
            message += '???????????????? ?????????????????????????? ?? ????????. ' \
                       '?????????????????????? ?????????????????????? ?????????????????????? ?????????????????? ?? ???????? ??????????.' \
                       ' ???????????????????? ???????????????????????????? ?????? ???????????? ???????????? ??????????.' \
                       ' ???????????????????? ?????????????????????????? ?? ????????????????????'
        else:
            message += '?????????????????????? ?????????????????????? ?? ???????? ?? ?????????? ??????????????????. ' \
                       '???????????????????? ?????????????????? ?????????????????????? ???? ?????????????? ?? ?????????????????? ????????????.' \
                       ' ?????????????????????? ???????????? ?????????????????? ???????? ????????????????'
        Test8.objects.create(user=request.user, self_rating=self_rating)
    return render(request, 'test_page.html',
                  {'test': about_tests['test8'], 'message': message})


@login_required(login_url='login')
def test9(request):
    message = None
    if request.method == 'POST':
        data = forms.Form(request.POST).data
        # ????????????????????
        answers = {i: int(data[str(i)]) for i in [2, 6, 8, 9, 10]}
        # ????????????????????
        answers.update({i: 8 - int(data[str(i)]) for i in [3, 5]})

        personal = sum(answers[i] for i in [3, 5, 8])
        eventful = sum(answers[i] for i in [6, 9])
        existential = sum(answers[i] for i in [2, 10])
        general = sum(answers.values())

        message = ''
        for name, answers, number in zip(
            ['?????????? ?????????????????????? ??????????????????????????', '?????????? ?????????????????????? ??????????????????????????',
             '?????????? ?????????????????????????????????? ??????????????????????????', '?????????? ???????????????????? ??????????????????????????'],
            [personal_answers, eventful_answers, existential_answers, general_answers],
            [personal, eventful, existential, general]
        ):
            message += f'{name}:\n'
            message += next(ans for scale, ans in answers.items() if number <= scale)
            message += '\n\n'
        Test9.objects.create(user=request.user, personal=personal,
                             eventful=eventful, existential=existential,
                             general=general)

    return render(request, 'test_page.html',
                  {'test': about_tests['test9'], 'message': message})


@login_required(login_url='login')
def test10(request):
    message = None
    if request.method == 'POST':
        data = forms.Form(request.POST).data
        emotional = sum(int(data[str(i)]) for i in range(1, 4))
        social = sum(int(data[str(i)]) for i in range(4, 9))
        psycho = sum(int(data[str(i)]) for i in range(9, 15))
        general = emotional + social + psycho
        message = f'?????????????????????????? ????????????????????????: {emotional}/15\n' \
                  f'???????????????????? ????????????????????????: {social}/25\n' \
                  f'?????????????????????????????? ????????????????????????: {psycho}/30\n' \
                  f'?????????? ???????????????????? ????????????????????????: {general}/70\n\n'

        message += '?????????????????? ???????????????????????? ???? ??. ????????: '
        if all(int(data[str(i)]) in [0, 1] for i in range(1, 4)) and \
                sum(int(data[str(i)]) in [0, 1] for i in range(4, 15)) >= 6:
            message += '??????????????????'
        elif sum(int(data[str(i)]) in [4, 5] for i in range(1, 4)) >= 1 and \
                sum(int(data[str(i)]) in [4, 5] for i in range(4, 15)) >= 6:
            message += '??????????????????????'
        else:
            message += '?????????????????? ????????????????????????'

        message += '\n\n?????????????????????????? ???????????? ???????????????????? ????????????????????????: {}'.format(
            next(ans for scale, ans in general_resilience.items() if general <= scale)
        )
        Test10.objects.create(user=request.user, emotional=emotional,
                              social=social, psycho=psycho, general=general)
    return render(request, 'test_page.html',
                  {'test': about_tests['test10'], 'message': message})


@login_required(login_url='login')
def test11(request):
    message = None
    if request.method == 'POST':
        data = forms.Form(request.POST).data

        # count answers
        answers = {i: int(data[str(i)]) - 1 for i in
                   [3, 7, 11, 12, 20, 23, 24]}
        answers.update(
            {i: 4 - int(data[str(i)]) for i in
             [1, 2, 4, 5, 6, 8, 9, 10, 13, 14, 15, 16, 17, 18, 19, 21, 22]}
        )

        # count results
        general = sum(answers.values())
        involvement = sum(answers[i] for i in
                          [2, 3, 4, 8, 11, 12, 15, 19, 20, 21])
        control = sum(answers[i] for i in
                      [1, 5, 7, 10, 17, 18, 22, 23])
        taking_risk = sum(answers[i] for i in
                          [6, 9, 13, 14, 16, 24])

        counter = lambda minimum, medium, number:\
            next(mes for num, mes in zip([minimum, medium, float('inf')],
                                         ['????????????', '??????????????', '??????????????'])
                 if number <= num)
        message = '???????????????????? (???????????????????? ?????? ?????????? ?? ???????????????? 18-75):\n'
        for name, numbers, value in \
                zip(['?????????? ???????????????????? ????????????????????????????', '??????????????????????????', '????????????????', '???????????????? ??????????'],
                    [(39, 62), (17, 27), (12, 21), (8, 15)],
                    [general, involvement, control, taking_risk]):
            message += f'{name}: {counter(numbers[0], numbers[1], value)}\n'

        Test11.objects.create(user=request.user, involvement=involvement,
                              control=control, taking_risk=taking_risk,
                              general=general)
    return render(request, 'test_page.html',
                  {'test': about_tests['test11'], 'message': message})


@login_required(login_url='login')
def test12(request):
    message = None
    if request.method == 'POST':
        data = forms.Form(request.POST).data
        values = [int(v) for k, v in data.items() if k.isdigit()]
        burnout = sum(values)
        grade, text = next(answer for number, answer in burnout_answers.items()
                           if burnout <= number).values()
        message = f'?????? ?????????????? ??????????????????: {burnout}/{len(values) * 5}, ' \
                  f'{grade} ??????????????.\n{text}'
        Test12.objects.create(user=request.user, burnout=burnout)
    return render(request, 'test_page.html',
                  {'test': about_tests['test12'], 'message': message})


@login_required(login_url='login')
def test13(request):
    message = None
    if request.method == 'POST':
        data = forms.Form(request.POST).data
        satisfaction = sum(int(data[str(i)]) for i in range(1, 6))
        # ?????????? 9 - ????????????????
        happiness = sum(int(data[str(i)]) for i in range(6, 9)) +\
                    (8 - int(data['9']))
        message = '???????????????????? ?????????????????????????????????? ???????????? - {}\n' \
                  '???????????????????? ?????????????????????????? ?????????????? - {}'.format(
            next(grade for number, grade in satisfaction_answers.items() if satisfaction <= number),
            next(grade for number, grade in happiness_answers.items() if happiness <= number)
        )
        Test13.objects.create(user=request.user,
                              satisfaction=satisfaction, happiness=happiness)
    return render(request, 'test_page.html',
                  {'test': about_tests['test13'], 'message': message})


@login_required(login_url='login')
def staffroom(request):
    if not request.user.is_staff:
        return redirect('home')
    return render(request, 'staffroom.html', {'cur_page': 'staffroom'})


# ?????????????????? ?????????? ?????????????????????? ?????????????? ??????????????????????????.
# ?????????????? ?????? ?????????????? ?? ???????????????????????? ???????????????? ????????????????.
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

    file_to_send = ContentFile(f"?????????? ???????????????????? ????????????????????????: {len(users)}\n\n"
                               f"???????????? 1(??????????????????????: {len(group1)}):\n" + usernames1 +
                               "\n?????????????????????? ??????????:\n" + emails1 +
                               f"\n\n???????????? 2(??????????????????????: {len(group2)}):\n" + usernames2 +
                               "\n?????????????????????? ??????????:\n" + emails2)
    response = HttpResponse(file_to_send, 'text/plain')
    response['Content-Disposition'] = 'attachment; filename="experiment.txt"'
    return response
