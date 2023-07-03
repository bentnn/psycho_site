from .models import *
from .test_answers import *


def count_test1(data, user, via_telegram=False):
    audio = [2, 6, 7, 13, 15, 17, 20, 24, 26, 33, 34, 36, 37, 43, 46, 48]
    visual = [1, 5, 8, 10, 12, 14, 19, 21, 23, 27, 31, 32, 39, 40, 42, 45]
    kinest = [3, 4, 9, 11, 16, 18, 22, 25, 28, 29, 30, 35, 38, 41, 44, 47]

    counter = lambda array: sum(str(data.get(str(i))) == 'yes' for i in array)
    audio_res = counter(audio)
    visual_res = counter(visual)
    kinest_res = counter(kinest)
    message = f"Аудиальный канал восприятия: {audio_res}/{len(audio)}, " \
              f"Визуальный канал восприятия: {visual_res}/{len(visual)}, " \
              f"Кинестетический канал восприятия: {kinest_res}/{len(kinest)}"
    Test1.objects.create(user=user, audio=audio_res, visual=visual_res, kinest=kinest_res, message=message,
                         via_telegram=via_telegram)

    return message


def count_test2(data, user, via_telegram=False):
    rt = [3, 4, 6, 7, 9, 12, 13, 14, 17, 18]
    lt = [22, 23, 24, 25, 28, 29, 31, 32, 34, 35, 37, 38, 40]

    rt_res = 35 + sum(int(data.get(str(i))) if i in rt
                      else -int(data.get(str(i)))
                      for i in range(1, 21))
    lt_res = 35 + sum(int(data.get(str(i))) if i in lt
                      else -int(data.get(str(i)))
                      for i in range(21, 41))
    if rt_res <= 30:
        message = "Низкая реактивная тревожность"
    elif 31 <= rt_res <= 45:
        message = "Умеренная реактивная тревожность"
    else:
        message = "Высокая реактивная тревожность"
    if lt_res <= 30:
        message += ", низкая личностная тревожность"
    elif 31 <= lt_res <= 45:
        message += ", умеренная личностная тревожность"
    else:
        message += ", высокая личностная тревожность"

    Test2.objects.create(user=user, rt=rt_res, lt=lt_res, message=message, via_telegram=via_telegram)
    return message


def count_test3(data, user, via_telegram=False):
    ud = [1, 3, 4, 7, 8, 9, 10, 13, 15, 19]
    ud_res = sum(int(data.get(str(i))) if i in ud
                 else 5 - int(data.get(str(i)))
                 for i in range(1, 21))

    if ud_res <= 50:
        message = "У вас отсутствует депрессия"
    elif 51 <= ud_res <= 60:
        message = "У вас легкая депрессия ситуативного или невротического генеза"
    elif 61 <= ud_res <= 70:
        message = "У вас субдепрессивное состояние или маскированная депрессия"
    else:
        message = "У вас истинное депрессивное состояние"

    Test3.objects.create(user=user, ud=ud_res, message=message, via_telegram=via_telegram)
    return message


def count_test4(data, user, via_telegram=False):
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

    sum_of_res = activity_res + being_res + mood_res
    a_proc = activity_res / sum_of_res * 100
    b_proc = being_res / sum_of_res * 100
    m_proc = 100 - b_proc - a_proc
    message = "Активность = {}/7, " \
              "самочувствие = {}/7, " \
              "настроение = {}/7. " \
              "В процентном соотношении: активность - {:.2f}%, " \
              "самочувствие - {:.2f}%, " \
              "настроение - {:.2f}%". \
        format(activity_res, being_res, mood_res, a_proc, b_proc, m_proc)
    Test4.objects.create(user=user, activity=activity_res, being=being_res, mood=mood_res,
                         message=message, via_telegram=via_telegram)
    return message


def count_test5(data, user, via_telegram=False):
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
    message = '. '.join(message)
    Test5.objects.create(user=user, sincerity=sinc_res, extrav=extrav_res, neuro=neuro_res,
                         message=message, via_telegram=via_telegram)

    return message


def count_test6(data, user, via_telegram=False):

    def count_message_test6(effect: int, low: int, middle: int,
                            name_of_effect: str):
        if effect <= low:
            msg = 'Низкий'
        elif effect <= middle:
            msg = 'Средний'
        else:
            msg = 'Высокий'
        return msg + f' уровень {name_of_effect} аффекта.\n'

    positive_effect = sum(int(data[str(i)]) for i in [1, 3, 5, 9, 10, 12, 14, 16, 17, 19])
    negative_effect = sum(int(data[str(i)]) for i in [2, 4, 6, 7, 8, 11, 13, 15, 18, 20])

    message = 'У вас:\n'
    message += count_message_test6(positive_effect, 22, 39, 'позитивного')
    message += count_message_test6(negative_effect, 15, 32, 'негативного')
    message += '\nВысокий уровень позитивного аффекта – состояние приятной вовлеченности, ' \
               'высокой энергичности и полной концентрации. Низкий уровень - состояние уныния и вялости.\n\n' \
               'Высокий уровень негативного аффекта – состояние субъективно переживаемого страдания, ' \
               'неприятной вовлеченности (различной по содержанию – это может быть гнев, отвращение, презрение, ' \
               'вина, страх, раздражительность). Низкий уровень - состояние спокойствия и безмятежности.'
    Test6.objects.create(user=user, positive_effect=positive_effect,
                         negative_effect=negative_effect, message=message, via_telegram=via_telegram)
    return message


def count_test7(data, user, via_telegram=False):
    counter = lambda array: sum(int(data[str(i)]) for i in array)
    depression = counter([3, 5, 10, 13, 16, 17, 21])
    anxiety = counter([2, 4, 7, 9, 15, 19, 20])
    stress = counter([1, 6, 8, 11, 12, 14, 18])
    message = ''
    for name, answers, number in zip(
            ['Шкала депрессии', 'Шкала тревоги', 'Шкала стресса'],
            [depression_answers, anxiety_answers, stress_asnwers],
            [depression, anxiety, stress]
    ):
        message += f"{name}:\n"
        message += next(ans for scale, ans in answers.items() if number <= scale)
        message += '\n'
    Test7.objects.create(user=user, depression=depression,
                         anxiety=anxiety, stress=stress, message=message, via_telegram=via_telegram)
    return message


def count_test8(data, user, via_telegram=False):
    self_rating = sum(int(data[str(i)]) for i in [1, 3, 4, 7, 10]) + \
                  sum(3 - int(data[str(i)]) for i in [2, 5, 6, 8, 9])
    message = 'Ваша самооценка на данный момент:\n'
    if self_rating <= 15:
        message += 'Ощущение неуверенности в себе. ' \
                   'Болезненное переживание критических замечаний в свой адрес.' \
                   ' Склонность подстраиваться под мнение других людей.' \
                   ' Избыточная застенчивость и скромность'
    else:
        message += 'Переживание уверенности в себе и своих поступках. ' \
                   'Склонность адекватно реагировать на критику и замечания других.' \
                   ' Способность трезво оценивать свои действия'
    Test8.objects.create(user=user, self_rating=self_rating, message=message, via_telegram=via_telegram)
    return message


def count_test9(data, user, via_telegram=False):
    # восходящие
    answers = {i: int(data[str(i)]) for i in [2, 6, 8, 9, 10]}
    # нисходящие
    answers.update((i, 8 - int(data[str(i)])) for i in [3, 5])

    personal = sum(answers[i] for i in [3, 5, 8])
    eventful = sum(answers[i] for i in [6, 9])
    existential = sum(answers[i] for i in [2, 10])
    general = sum(answers.values())

    message = ''
    for name, answers, number in zip(
            ['Шкала личностного самообладания', 'Шкала событийного самообладания',
             'Шкала экзистенциального самообладания', 'Общий показатель самообладания'],
            [personal_answers, eventful_answers, existential_answers, general_answers],
            [personal, eventful, existential, general]
    ):
        message += f'{name}:\n'
        message += next(ans for scale, ans in answers.items() if number <= scale)
        message += '\n\n'
    Test9.objects.create(user=user, personal=personal,
                         eventful=eventful, existential=existential,
                         general=general, message=message, via_telegram=via_telegram)
    return message


def count_test10(data, user, via_telegram=False):
    emotional = sum(int(data[str(i)]) for i in range(1, 4))
    social = sum(int(data[str(i)]) for i in range(4, 9))
    psycho = sum(int(data[str(i)]) for i in range(9, 15))
    general = emotional + social + psycho
    message = f'Эмоциональное благополучие: {emotional}/15\n' \
              f'Социальное благополучие: {social}/25\n' \
              f'Психологическое благополучие: {psycho}/30\n' \
              f'Общий показатель благополучия: {general}/70\n\n'

    message += 'Состояние благополучия по К. Кизу: '
    if all(int(data[str(i)]) in [0, 1] for i in range(1, 4)) and \
            sum(int(data[str(i)]) in [0, 1] for i in range(4, 15)) >= 6:
        message += 'угнетение'
    elif sum(int(data[str(i)]) in [4, 5] for i in range(1, 4)) >= 1 and \
            sum(int(data[str(i)]) in [4, 5] for i in range(4, 15)) >= 6:
        message += 'процветание'
    else:
        message += 'умеренное благополучие'

    message += '\n\nИнтерпритация общего показателя благополучия: {}'.format(
        next(ans for scale, ans in general_resilience.items() if general <= scale)
    )
    Test10.objects.create(user=user, emotional=emotional,
                          social=social, psycho=psycho, general=general, message=message, via_telegram=via_telegram)
    return message


def count_test11(data, user, via_telegram=False):
    # count answers
    answers = {i: int(data[str(i)]) - 1 for i in [3, 7, 11, 12, 20, 23, 24]}
    answers.update(
        (i, 4 - int(data[str(i)])) for i in [1, 2, 4, 5, 6, 8, 9, 10, 13, 14, 15, 16, 17, 18, 19, 21, 22]
    )

    # count results
    general = sum(answers.values())
    involvement = sum(answers[i] for i in
                      [2, 3, 4, 8, 11, 12, 15, 19, 20, 21])
    control = sum(answers[i] for i in
                  [1, 5, 7, 10, 17, 18, 22, 23])
    taking_risk = sum(answers[i] for i in
                      [6, 9, 13, 14, 16, 24])

    counter = lambda minimum, medium, number: \
        next(mes for num, mes in zip([minimum, medium, float('inf')],
                                     ['низкий', 'средний', 'высокий'])
             if number <= num)
    message = 'Показатели (актуальный для людей в возрасте 18-75):\n'
    for name, numbers, value in \
            zip(['Общий показатель жизнестойкости', 'Вовлеченность', 'Контроль', 'Принятие риска'],
                [(39, 62), (17, 27), (12, 21), (8, 15)],
                [general, involvement, control, taking_risk]):
        message += f'{name}: {counter(numbers[0], numbers[1], value)}\n'

    Test11.objects.create(user=user, involvement=involvement,
                          control=control, taking_risk=taking_risk,
                          general=general, message=message, via_telegram=via_telegram)
    return message


def count_test12(data, user, via_telegram=False):
    values = [int(v) for k, v in data.items() if k.isdigit()]
    burnout = sum(values)
    grade, text = next(answer for number, answer in burnout_answers.items()
                       if burnout <= number).values()
    message = f'Ваш уровень выгорания: {burnout}/{len(values) * 5}, ' \
              f'{grade} уровень.\n{text}'
    Test12.objects.create(user=user, burnout=burnout, message=message, via_telegram=via_telegram)
    return message


def count_test13(data, user, via_telegram=False):
    satisfaction = sum(int(data[str(i)]) for i in range(1, 6))
    # Пункт 9 - обратный
    happiness = sum(int(data[str(i)]) for i in range(6, 9)) + (8 - int(data['9']))
    message = 'Показатель удовлетворенности жизнью - {}\n' \
              'Показатель субъективного счастья - {}'.format(
        next(grade for number, grade in satisfaction_answers.items() if satisfaction <= number),
        next(grade for number, grade in happiness_answers.items() if happiness <= number)
    )
    Test13.objects.create(user=user, satisfaction=satisfaction,
                          happiness=happiness, message=message, via_telegram=via_telegram)
    return message
