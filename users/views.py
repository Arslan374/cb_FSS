from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Profile
from django.contrib import messages

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserRegisterForm, ProfileRegisterForm


def register(request):
    if request.method == 'POST':
        u_form = UserRegisterForm(request.POST)
        if u_form.is_valid():
            u_form.save()
            username = u_form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            if not request.user.is_superuser:
                user.is_active = False
            user.save()
            p_form = ProfileRegisterForm(request.POST,
                                         request.FILES,
                                         instance=user.profile)
            if p_form.is_valid():
                p_form.save()
                messages.success(
                    request, f'Account with username [{username}] created!')
            else:
                user.delete()
                messages.error(
                    request, f'Please Fill the form again. Some fields are missing!')
            return redirect('home')
        else:
            messages.error(
                request, f'Please Fill the form again. Some fields are missing!')

    u_form = UserRegisterForm()
    p_form = ProfileRegisterForm()

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/register.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('pmal-home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {
        'form': form
    })