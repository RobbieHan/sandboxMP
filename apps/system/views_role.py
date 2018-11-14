# @Time   : 2018/11/13 23:25
# @Author : RobbieHan
# @File   : views_role.py

import json

from django.views.generic.base import View
from django.shortcuts import HttpResponse
from django.views.generic import TemplateView

from .mixin import LoginRequiredMixin
from .models import Role
from custom import SandboxCreateView, SandboxUpdateView


class RoleView(LoginRequiredMixin, TemplateView):
    template_name = 'system/role.html'


class RoleCreateView(SandboxCreateView):
    model = Role
    fields = '__all__'


class RoleListView(LoginRequiredMixin, View):

    def get(self, reqeust):
        fields = ['id', 'name', 'desc']
        ret = dict(data=list(Role.objects.values(*fields)))
        return HttpResponse(json.dumps(ret), content_type='application/json')


class RoleUpdateView(SandboxUpdateView):
    model = Role
    fields = '__all__'
    template_name_suffix = '_update'
