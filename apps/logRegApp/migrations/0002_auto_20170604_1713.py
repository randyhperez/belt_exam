# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-04 21:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logRegApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='fName',
            new_name='name',
        ),
    ]