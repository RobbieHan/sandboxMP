# @Time   : 2018/11/9 12:24
# @Author : RobbieHan
# @File   : views.menu.py

from django.views.generic import ListView, UpdateView

from .mixin import LoginRequiredMixin
from apps.custom import SimpleInfoCreateView
from .models import Menu


class MenuCreateView(SimpleInfoCreateView):
    model = Menu
    fields = '__all__'
    extra_context = dict(menu_all=Menu.objects.all())


class MenuListView(LoginRequiredMixin, ListView):
    model = Menu
    context_object_name = 'menu_all'
