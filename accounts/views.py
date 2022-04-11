from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, logout, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import mixins, backends
from django.contrib.auth import models

from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views


# Create your views here.

class DashBoard(TemplateView):
    template_name = 'registration/dashboard.html'


class LoginView(auth_views.LoginView):
    redirect_authenticated_user = False
    redirect_field_name = 'next'
    next_page = ''


class LogoutView(auth_views.LogoutView):
    pass


def my_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
