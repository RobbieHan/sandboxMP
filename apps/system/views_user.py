# @Time   : 2018/10/16 23:11
# @Author : RobbieHan
# @File   : views_user.py

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from .forms import LoginForm
from .mixin import LoginRequiredMixin


class IndexView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'index.html')


class LoginView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'system/users/login.html')
        else:
            return HttpResponseRedirect('/')

    def post(self, request):
        redirect_to = request.GET.get('next', '/')
        login_form = LoginForm(request.POST)
        ret = dict(login_form=login_form)
        if login_form.is_valid():
            user_name = request.POST['username']
            pass_word = request.POST['password']
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(redirect_to)
                else:
                    ret['msg'] = '用户未激活！'
            else:
                ret['msg'] = '用户名或密码错误！'
        else:
            ret['msg'] = '用户和密码不能为空！'
        return render(request, 'system/users/login.html', ret)


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('login'))