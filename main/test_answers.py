# test 8
depression_answers = {
    0: 'Отсутствие переживаний депрессивного спектра',
    8: 'Переживания симптомов депрессивного спектра от легкой депрессии'
       ' (субдепрессии) до выраженной депрессии средней тяжести',
    float('inf'):
        'Тяжелая депрессия. Переживание апатии и ангедонии. '
        'Ощущение безнадежности и бессмысленности жизни. '
        'Отсутствие интереса ко всем занятиям. '
        'Склонность к самоуничтожению и суицидальным мыслям. '
        'Раздражительность и плохое настроение. Нарушение сна и плохой аппетит'
}
anxiety_answers = {
    0: 'Отсутствие тревожных переживаний',
    7: 'Наличие тревожных переживаний от легких '
       'до клинически выраженной тревоги',
    float('inf'):
        'Высокая степень тревоги. Переживание сильного возбуждения и перенапряжения.'
        ' Ожидание отрицательных событий, трудноопределимые предчувствия'
}
stress_asnwers = {
    2: 'Отсутствие симптомов состояния стресса',
    10: 'Наличие стресса. Переживания от легкого напряжения до '
        'нагрузки высокой степени интенсивности',
    float('inf'):
        'Сильный стресс. Переживание нервного возбуждения и раздражительности.'
        ' Состояние повышенного напряжения. Неспособность расслабиться'
}

# test 9

personal_answers = {
    10: 'Подверженность стрессам повседневной жизни. '
        'Риск внезапной утраты контроля над самим собой сохраняется даже в '
        'привычных обстоятельствах',
    19: 'Сдержанность, умеренность. '
        'Потеря самообладания происходит только в ситуации хронического стресс',
    float('inf'):
        'Уверенность в собственных силах, настойчивость, упорство. '
        'Способность к самообладанию проявляется в широком репертуаре '
        'различных жизненных обстоятельств'
}

eventful_answers = {
    6: 'Страх неизвестности, склонность к паникерству и пассивности, '
       'избегание неопределенных или сложных жизненных ситуаций',
    12: 'Присутствие самообладания в непривычных ситуациях. '
        'Чувства растерянности и беспомощности возникают при '
        'столкновении с чрезмерными ситуативными нагрузками',
    float('inf'):
        'Принятие сложности и непредсказуемости окружающего мира. '
        'Контроль над своими чувствами, мыслями и поступками сохраняется в '
        'ситуациях любой сложности'
}

existential_answers = {
    5: 'Психологическая незрелость, ощущение хаоса. '
       'Власть над самим собой и своей жизнью воспринимается как тяжкое бремя',
    11: 'Потребность в гармонии и порядке. '
        'Экзистенциальные переживания провоцируют либо уход в '
        'отрицание ответственности, либо переход к ее принятию',
    float('inf'):
        'Мудрость, осознанность, интуитивное постижение окружающего мира. '
        'Самообладание является жизненной философией'
}

general_answers = {
    24: 'Нереальная связь с миром (предрасположенность к зависимостям), '
        'потребность в контроле извне. Потеря самообладания колеблется в своих '
        'проявлениях от пристрастности и импульсивности до заторможенности, смирения и кротости',
    40: 'Чуткое отношение к своим потребностям. '
        'Душевное равновесие достигается путем постоянного включения «внутреннего цензора»',
    float('inf'):
        'Переживание реальности, ощущение гармонии, интуитивноепостижение мира.'
        ' Признаниесобственных противоречийсочетается со '
        'стремлением к целостности и совершенству'
}

# test 11

general_resilience = {
    8: 'очень низкие баллы',
    23: 'существенно ниже среднего',
    35: 'несколько ниже среднего',
    48: 'несколько выше среднего',
    62: 'существенно выше среднего',
    float('inf'): 'очень высокие баллы'
}

# test 12

burnout_answers = {
    26: {
        'grade': 'низкий',
        'text': 'Вера в ценность учебной деятельности. '
                'Внутренняя мотивация. Вера в свои силы, ощущение контроля. '
                'Осмысленность и интерес к учебе'
    },
    40: {
        'grade': 'средний',
        'text': 'Снижение интереса к учебе. '
                'Появление сомнений в смысле и важности обучения. '
                'Чувство бессилия при столкновении с чрезмерными нагрузками'
    },
    float('inf'): {
        'grade': 'высокий',
        'text': 'Отсутствие веры в значимость и необходимость учебной деятельности. '
                'Склонность считать все прилагаемые усилия тщетными. '
                'Признание бессмысленности обучения и активность, '
                'направленная на занятие деструктивной позиции. '
                'Склонность к риску и авантюрам (использование шпаргалок и т.п.). '
                'Амотивация'
    }
}

satisfaction_answers = {
    14: 'низкий',
    27: 'умеренный ',
    float('inf'): 'высокий'
}

happiness_answers = {
    13: 'низкий',
    23: 'умеренный ',
    float('inf'): 'высокий'
}
