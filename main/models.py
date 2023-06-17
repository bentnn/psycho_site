from django.db import models
from django.contrib.auth.models import User


class BaseTestModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    via_telegram = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Test1(BaseTestModel):
    audio = models.IntegerField()
    visual = models.IntegerField()
    kinest = models.IntegerField()


class Test2(BaseTestModel):
    rt = models.IntegerField()
    lt = models.IntegerField()


class Test3(BaseTestModel):
    ud = models.IntegerField()


class Test4(BaseTestModel):
    activity = models.IntegerField()
    being = models.IntegerField()
    mood = models.IntegerField()


class Test5(BaseTestModel):
    sincerity = models.IntegerField()
    extrav = models.IntegerField()
    neuro = models.IntegerField()


class Test6(BaseTestModel):
    positive_effect = models.IntegerField()
    negative_effect = models.IntegerField()


class Test7(BaseTestModel):
    depression = models.IntegerField()
    anxiety = models.IntegerField()
    stress = models.IntegerField()


class Test8(BaseTestModel):
    self_rating = models.IntegerField()


class Test9(BaseTestModel):
    personal = models.IntegerField()
    eventful = models.IntegerField()
    existential = models.IntegerField()
    general = models.IntegerField()


class Test10(BaseTestModel):
    emotional = models.IntegerField()
    social = models.IntegerField()
    psycho = models.IntegerField()
    general = models.IntegerField()


class Test11(BaseTestModel):
    involvement = models.IntegerField()
    control = models.IntegerField()
    taking_risk = models.IntegerField()
    general = models.IntegerField()


class Test12(BaseTestModel):
    burnout = models.IntegerField()


class Test13(BaseTestModel):
    satisfaction = models.IntegerField()
    happiness = models.IntegerField()
