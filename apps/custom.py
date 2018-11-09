# @Time   : 2018/11/9 22:06
# @Author : RobbieHan
# @File   : custom.py

import json

from django.views.generic import CreateView
from django.shortcuts import HttpResponse

from system.mixin import LoginRequiredMixin


class SimpleInfoCreateView(LoginRequiredMixin, CreateView):

    def post(self, request, *args, **kwargs):
        res = dict(result=False)
        form = self.get_form()
        if form.is_valid():
            form.save()
            res['result'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')
