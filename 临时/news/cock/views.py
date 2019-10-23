from django.shortcuts import render

from database import *


def index(request):
    return render(request, 'index.html')
