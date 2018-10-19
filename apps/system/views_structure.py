# @Time   : 2018/10/18 23:04
# @Author : RobbieHan
# @File   : views_structure.py

import json

from django.views.generic.base import TemplateView
from django.views.generic.base import View
from django.shortcuts import render
from django.shortcuts import HttpResponse

from .mixin import LoginRequiredMixin
from .models import Structure
from .forms import StructureForm


class StructureView(LoginRequiredMixin, TemplateView):

    template_name = 'system/structure/structure.html'


class StructureCreateView(LoginRequiredMixin, View):

    def get(self, request):
        ret = dict(structure_all=Structure.objects.all())
        return render(request, 'system/structure/structure_create.html', ret)

    def post(self, request):
        res = dict(result=False)
        structure = Structure()
        structure_form = StructureForm(request.POST, instance=structure)
        if structure_form.is_valid():
            structure_form.save()
            res['result'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')
