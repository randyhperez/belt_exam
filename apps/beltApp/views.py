# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from ..logRegApp.models import Users

# Create your views here.
def index(request):
    return render(request, 'beltApp/index.html')
