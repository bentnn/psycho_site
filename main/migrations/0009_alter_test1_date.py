# Generated by Django 3.2.3 on 2021-10-04 11:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20210726_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test1',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 20, 12, 0)),
        ),
    ]
