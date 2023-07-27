from django.db import models
from django.contrib.auth.models import User


class BaseTestModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    message = models.TextField(default='')
    via_telegram = models.BooleanField(default=False)

    resulting_fields = ()

    class Meta:
        abstract = True


class Test1(BaseTestModel):
    audio = models.IntegerField(verbose_name='Аудиальный')
    visual = models.IntegerField(verbose_name='Визуальный')
    kinest = models.IntegerField(verbose_name='Кинестетический')
    resulting_fields = ('audio', 'visual', 'kinest')


class Test2(BaseTestModel):
    rt = models.IntegerField(verbose_name='Реактивная')
    lt = models.IntegerField(verbose_name='Личностная')
    resulting_fields = ('rt', 'lt')


class Test3(BaseTestModel):
    ud = models.IntegerField(verbose_name='Уровень депрессии')
    resulting_fields = ('ud',)


class Test4(BaseTestModel):
    activity = models.IntegerField(verbose_name='Активность')
    being = models.IntegerField(verbose_name='Самочувствие')
    mood = models.IntegerField(verbose_name='Настроение')
    resulting_fields = ('activity', 'being', 'mood')


class Test5(BaseTestModel):
    sincerity = models.IntegerField(verbose_name='Искренность')
    extrav = models.IntegerField(verbose_name='Экстровертность')
    neuro = models.IntegerField(verbose_name='Невротизм')
    resulting_fields = ('sincerity', 'extrav', 'neuro')


class Test6(BaseTestModel):
    positive_effect = models.IntegerField(verbose_name='Позитивный аффект')
    negative_effect = models.IntegerField(verbose_name='Негативный аффект')
    resulting_fields = ('positive_effect', 'negative_effect')


class Test7(BaseTestModel):
    depression = models.IntegerField(verbose_name='Депрессивность')
    anxiety = models.IntegerField(verbose_name='Тревога')
    stress = models.IntegerField(verbose_name='Стресс')
    resulting_fields = ('depression', 'anxiety', 'stress')


class Test8(BaseTestModel):
    self_rating = models.IntegerField(verbose_name='Самооценка')
    resulting_fields = ('self_rating',)


class Test9(BaseTestModel):
    personal = models.IntegerField(verbose_name='Личностное самообладание')
    eventful = models.IntegerField(verbose_name='Событийное самообладание')
    existential = models.IntegerField(verbose_name='Экзистенциальное самообладание')
    general = models.IntegerField(verbose_name='Общее самообладание')
    resulting_fields = ('personal', 'eventful', 'existential', 'general')


class Test10(BaseTestModel):
    emotional = models.IntegerField(verbose_name='Эмоциональное благополучие')
    social = models.IntegerField(verbose_name='Социальное благополучие')
    psycho = models.IntegerField(verbose_name='Психологическое благополучие')
    general = models.IntegerField(verbose_name='Общее благополучие')
    resulting_fields = ('emotional', 'social', 'psycho', 'general')


class Test11(BaseTestModel):
    involvement = models.IntegerField(verbose_name='Вовлеченность')
    control = models.IntegerField(verbose_name='Контроль')
    taking_risk = models.IntegerField(verbose_name='Принятие риска')
    general = models.IntegerField(verbose_name='Общая жизнестойкость')
    resulting_fields = ('involvement', 'control', 'taking_risk', 'general')


class Test12(BaseTestModel):
    burnout = models.IntegerField(verbose_name='Уровень выгорания')
    resulting_fields = ('burnout',)


class Test13(BaseTestModel):
    satisfaction = models.IntegerField(verbose_name='Удовлетворенность жизнью')
    happiness = models.IntegerField(verbose_name='Субъективное счастье')
    resulting_fields = ('satisfaction', 'happiness')
