from django.shortcuts import render
from django.views.generic.base import View

from .mixin import LoginRequiredMixin


class SystemView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'system/system_index.html')

