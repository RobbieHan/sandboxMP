# @Time   : 2018/11/13 23:25
# @Author : RobbieHan
# @File   : views_role.py

import json

from django.views.generic.base import View
from django.shortcuts import HttpResponse, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.shortcuts import render

from .mixin import LoginRequiredMixin
from .models import Role, Menu
from custom import SandboxCreateView, SandboxUpdateView, BreadcrumbMixin

User = get_user_model()


class RoleView(LoginRequiredMixin, BreadcrumbMixin, TemplateView):
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


class RoleDeleteView(LoginRequiredMixin, View):

    def post(self, request):
        ret = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            id_list = map(int, request.POST['id'].split(','))
            Role.objects.filter(id__in=id_list).delete()
            ret['result'] = True
        return HttpResponse(json.dumps(ret), content_type='application/json')


class Role2UserView(LoginRequiredMixin, View):
    """
    角色关联用户
    """

    def get(self, request):
        if 'id' in request.GET and request.GET['id']:
            role = get_object_or_404(Role, pk=int(request.GET.get('id')))
            added_users = role.userprofile_set.all()
            all_users = User.objects.all()
            un_add_users = set(all_users).difference(added_users)
            ret = dict(role=role, added_users=added_users, un_add_users=list(un_add_users))
        return render(request, 'system/role_role2user.html', ret)

    def post(self, request):
        res = dict(result=False)
        id_list = None
        role = get_object_or_404(Role, pk=int(request.POST.get('id')))
        if 'to' in request.POST and request.POST['to']:
            id_list = map(int, request.POST.getlist('to', []))
        role.userprofile_set.clear()
        if id_list:
            for user in User.objects.filter(id__in=id_list):
                role.userprofile_set.add(user)
        res['result'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')


class Role2MenuView(LoginRequiredMixin, View):
    """
    角色绑定菜单
    """
    def get(self, request):
        if 'id' in request.GET and request.GET['id']:
            role = get_object_or_404(Role, pk=request.GET['id'])
            ret = dict(role=role)
            return render(request, 'system/role_role2menu.html', ret)

    def post(self, request):
        res = dict(result=False)
        role = get_object_or_404(Role, pk=request.POST['id'])
        tree = json.loads(self.request.POST['tree'])
        role.permissions.clear()
        for menu in tree:
            if menu['checked'] is True:
                menu_checked = get_object_or_404(Menu, pk=menu['id'])
                role.permissions.add(menu_checked)
        res['result'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')


class Role2MenuListView(LoginRequiredMixin, View):
    """
    获取zTree菜单列表
    """
    def get(self, request):
        fields = ['id', 'name', 'parent']
        if 'id' in request.GET and request.GET['id']:
            role = Role.objects.get(id=request.GET.get('id'))
            role_menus = role.permissions.values(*fields)
            ret = dict(data=list(role_menus))
        else:
            menus = Menu.objects.all()
            ret = dict(data=list(menus.values(*fields)))
        return HttpResponse(json.dumps(ret), content_type='application/json')