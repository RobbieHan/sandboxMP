# @Time   : 2018/11/9 12:24
# @Author : RobbieHan
# @File   : views.menu.py

from apps.custom import SimpleInfoCreateView
from .models import Menu


class MenuCreateView(SimpleInfoCreateView):
    model = Menu
    fields = '__all__'
    extra_context = dict(menu_all=Menu.objects.all())





