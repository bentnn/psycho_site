# Generated by Django 3.2.3 on 2021-10-04 11:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20211004_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test1',
            name='date',
            field=models.DateField(default=datetime.date(2021, 7, 20)),
        ),
    ]