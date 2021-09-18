
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, Div
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from users.models import Profile, User


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'username']

    username = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def clean_email(self):
        return self.initial['email']

    def clean_username(self):
        return self.initial['username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.field_class = 'input-sm col-xs-6 md-0'
        self.helper.layout = Layout(
            Div(
                Div('username', css_class='col'),
                Div('email', css_class='col'),
                
                Div('first_name', css_class='col'),
                Div('last_name', css_class='col'),
                
            ),
        )


class ProfileUpdateForm(forms.ModelForm):
    subscription = forms.DateField(widget=forms.DateInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Profile
        fields = ['gender', 'phone', 'subscription']
        address = forms.CharField(widget=forms.TextInput())

    def clean_account_type(self):
        return self.initial['account_type']

    def clean_ref(self):
        return self.initial['ref']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.field_class = 'input-sm col-xs-6 md-0'
        self.helper.layout = Layout(
            Div(
                Div('gender', css_class='col'),
                Div('phone', css_class='col'),
                Div('subscription', css_class='col'),
        )
        )


@login_required
def update_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('home')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
