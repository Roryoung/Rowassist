# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-08-20 21:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RA', '0003_userprofile_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='name',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='profilePic',
        ),
    ]