# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-16 04:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Train_Result',
            fields=[
                ('headline', models.TextField(max_length=500, primary_key=True)),
                ('bodyid', models.IntegerField(primary_key=True, serialize=False)),
                ('stance1', models.FloatField()),
                ('stance2', models.FloatField()),
                ('stance3', models.FloatField()),
                ('stance4', models.FloatField()),
            ],
        ),
    ]
