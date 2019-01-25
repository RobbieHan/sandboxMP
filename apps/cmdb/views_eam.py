from django.views.generic import TemplateView

from system.mixin import LoginRequiredMixin
from custom import (BreadcrumbMixin, SandboxDeleteView,
                    SandboxListView, SandboxUpdateView, SandboxCreateView)
from .models import Cabinet


class CabinetView(LoginRequiredMixin, BreadcrumbMixin, TemplateView):
    template_name = 'cmdb/cabinet.html'


class CabinetCreateView(SandboxCreateView):
    model = Cabinet
    fields = '__all__'


class CabinetUpdateView(SandboxUpdateView):
    model = Cabinet
    fields = '__all__'


class CabinetListView(SandboxListView):
    model = Cabinet
    fields = ['id', 'number', 'position', 'desc']

    def get_filters(self):
        data = self.request.GET
        filters = {}
        if 'number' in data and data['number']:
            filters['number__icontains'] = data['number']
        if 'position' in data and data['position']:
            filters['position__icontains'] = data['position']
        return filters


class CabinetDeleteView(SandboxDeleteView):
    model = Cabinet
