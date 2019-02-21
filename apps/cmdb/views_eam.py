import re

from django.views.generic import TemplateView, View
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.shortcuts import render
from django.forms.models import model_to_dict

from system.mixin import LoginRequiredMixin
from custom import (BreadcrumbMixin, SandboxDeleteView,
                    SandboxListView, SandboxUpdateView, SandboxCreateView)
from .models import Cabinet, DeviceInfo, Code, ConnectionInfo, DeviceFile
from .forms import DeviceCreateForm, DeviceUpdateForm, ConnectionInfoForm, DeviceFileUploadForm
from utils.db_utils import MongodbDriver
from utils.sandbox_utils import LoginExecution

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


class Device2ConnectionView(LoginRequiredMixin, View):

    def get(self, request):
        ret = dict()
        if 'id' in request.GET and request.GET['id']:
            device = get_object_or_404(DeviceInfo, pk=int(request.GET['id']))
            ret['device'] = device
            dev_connection = device.dev_connection
            if dev_connection:
                connection_info = get_object_or_404(
                    ConnectionInfo, pk=int(dev_connection)
                )
                ret['connection_info'] = connection_info
        return render(request, 'cmdb/deviceinfo2connection.html', ret)

    def post(self, request):
        res = dict(result=False)
        con_info = ConnectionInfo()
        if 'id' in request.POST and request.POST['id']:
            con_info = get_object_or_404(ConnectionInfo, pk=request.POST['id'])
        form = ConnectionInfoForm(request.POST, instance=con_info)
        if form.is_valid():
            instance = form.save()
            con_id = getattr(instance, 'id')
            device = get_object_or_404(DeviceInfo, hostname=request.POST['hostname'])
            device.dev_connection = con_id
            device.save()
            res['result'] = True
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            form_errors = str(form.errors)
            errors = re.findall(pattern, form_errors)
            res['error'] = errors[0]
        return JsonResponse(res)


class DeviceDetailView(LoginRequiredMixin, BreadcrumbMixin, TemplateView):
    template_name = 'cmdb/deviceinfo_detail.html'

    def get_context_data(self, **kwargs):
        device = get_object_or_404(DeviceInfo, pk=int(self.request.GET['id']))
        mongo = MongodbDriver()
        logs = mongo.find(id=int(self.request.GET['id']), sort_by='history_date')
        all_file = device.devicefile_set.all()
        device_public = get_device_public()
        kwargs['device'] = device
        kwargs['logs'] = logs
        kwargs['all_file'] = all_file
        kwargs.update(device_public)
        return super().get_context_data(**kwargs)


class DeviceFileUploadView(LoginRequiredMixin, View):

    def get(self, request):
        ret = dict()
        device = get_object_or_404(DeviceInfo, pk=request.GET['id'])
        ret['device'] = device
        return render(request, 'cmdb/deviceinfo_upload.html', ret)

    def post(self, request):
        res = dict(result=False)
        device_file = DeviceFile()
        upload_form = DeviceFileUploadForm(
            request.POST, request.FILES, instance=device_file
        )
        if upload_form.is_valid():
            upload_form.save()
            res['result'] = True
        return JsonResponse(res)


class DeviceFileDeleteView(SandboxDeleteView):
    model = DeviceFile


class AutoUpdateDeviceInfo(LoginRequiredMixin, View):

    def post(self, request):
        res = dict(status='fail')
        if 'id' in request.POST and request.POST['id']:
            device = get_object_or_404(DeviceInfo, pk=int(request.POST['id']))
            con_id = device.dev_connection
            conn = ConnectionInfo.objects.filter(id=con_id)
            if con_id and conn:
                try:
                    conn_info = conn.get()
                    kwargs = model_to_dict(conn_info, exclude=['id', 'auth_type'])
                    auth_type = conn_info.auth_type
                    le = LoginExecution()
                    data = le.login_execution(auth_type=auth_type, **kwargs)
                    conn_info.status = data['status']
                    conn_info.save()
                    if data['status'] == 'succeed':
                        device.sys_hostname = data['sys_hostname']
                        device.mac_address = data['mac_address']
                        device.sn_number = data['sn_number']
                        device.os_type = data['os_type']
                        device.device_type = data['device_type']
                        device.save()
                        res['status'] = 'success'
                except conn.model.DoesNotExist:
                    res['status'] = 'con_empty'
            else:
                res['status'] = 'con_empty'
        return JsonResponse(res)
