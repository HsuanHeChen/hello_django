# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-30 07:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unionapp', '0003_auto_20171129_1559'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelFormFailureHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_data', models.TextField()),
                ('model_data', models.TextField()),
            ],
        ),
    ]