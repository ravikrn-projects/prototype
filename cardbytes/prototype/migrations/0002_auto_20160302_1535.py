# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-02 15:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prototype', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchant',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
