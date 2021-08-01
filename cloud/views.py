from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def home(request):
    context = {}
    context['name'] = request.user.get_full_name()
    return render(request, 'cloud/home.html', context)