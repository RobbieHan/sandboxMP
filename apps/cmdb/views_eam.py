from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from system.mixin import LoginRequiredMixin
from custom import (BreadcrumbMixin, SandboxDeleteView,
                    SandboxListView, SandboxUpdateView, SandboxCreateView)
from .models import Cabinet, DeviceInfo, Code
from .forms import DeviceCreateForm, DeviceUpdateForm

User = get_user_model()


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


def get_device_public():
    all_code = Code.objects.all()
    all_cabinet = Cabinet.objects.all()
    all_user = User.objects.all()
    all_device = DeviceInfo.objects.all()
    ret = {
        'all_code': all_code,
        'all_cabinet': all_cabinet,
        'all_user': all_user,
        'all_device': all_device,
    }
    return ret


class DeviceView(LoginRequiredMixin, BreadcrumbMixin, TemplateView):
    template_name = 'cmdb/deviceinfo.html'

    def get_context_data(self, **kwargs):
        device_public = get_device_public()
        kwargs.update(device_public)
        return super().get_context_data(**kwargs)


class DeviceListView(SandboxListView):
    model = DeviceInfo
    fields = ['id', 'sys_hostname', 'sn_number', 'os_type', 'device_type', 'hostname', 'mac_address', 'leader']

    def get_filters(self):
        data = self.request.GET
        filters = {}
        if 'sys_hostname' in data and data['sys_hostname']:
            filters['sys_hostname__icontains'] = data['sys_hostname']
        if 'hostname' in data and data['hostname']:
            filters['hostname__icontains'] = data['hostname']
        if 'network_type' in data and data['network_type']:
            filters['network_type'] = data['network_type']
        if 'service_type' in data and data['service_type']:
            filters['service_type'] = data['service_type']
        if 'operation_type' in data and data['operation_type']:
            filters['operation_type'] = data['operation_type']
        return filters

    def get_datatables_paginator(self, request):
        context_data = super().get_datatables_paginator(request)
        data = context_data['data']
        for device in data:
            user_id = device['leader']
            device['leader'] = get_object_or_404(
                User, pk=int(user_id)).name if user_id else ''
        return context_data


class DeviceCreateView(SandboxCreateView):
    model = DeviceInfo
    form_class = DeviceCreateForm

    def get_context_data(self, **kwargs):
        public_data = get_device_public()
        kwargs.update(public_data)
        print(public_data)
        return super().get_context_data(**kwargs)


class DeviceUpdateView(SandboxUpdateView):
    model = DeviceInfo
    form_class = DeviceUpdateForm

    def get_context_data(self, **kwargs):
        public_data = get_device_public()
        kwargs.update(public_data)
        return super().get_context_data(**kwargs)


class DeviceDeleteView(SandboxDeleteView):
    model = DeviceInfo
