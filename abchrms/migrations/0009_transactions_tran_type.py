# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-02 18:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abchrms', '0008_auto_20180702_2354'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='tran_type',
            field=models.CharField(default='undefined', max_length=20),
        ),
    ]
