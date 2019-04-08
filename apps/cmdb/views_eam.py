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
from .models import (Cabinet, DeviceInfo, Code, ConnectionInfo, DeviceFile,
                     Supplier, NetworkAsset, NatRule, DomainName)
from .forms import (DeviceCreateForm, DeviceUpdateForm, ConnectionInfoForm,
                    DeviceFileUploadForm, NetworkAssetForm,
                    NatRuleForm)
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
    fields = ['id', 'sys_hostname', 'hostname', 'service_type', 'operation_type', 'config', 'dev_cabinet',
              'network_type']

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
        if 'dev_cabinet' in data and data['dev_cabinet']:
            filters['dev_cabinet'] = data['dev_cabinet']
        return filters

    def get_datatables_paginator(self, request):
        context_data = super().get_datatables_paginator(request)
        data = context_data['data']
        for device in data:
            service_type = device['service_type']
            operation_type = device['operation_type']
            dev_cabinet = device['dev_cabinet']
            network_type = device['network_type']
            device['operation_type'] = get_object_or_404(Code, pk=int(operation_type)).value if operation_type else ''
            device['network_type'] = get_object_or_404(Code, pk=int(network_type)).value if network_type else ''
            device['service_type'] = get_object_or_404(Code, pk=int(service_type)).value if service_type else ''
            device['dev_cabinet'] = get_object_or_404(Cabinet, pk=int(dev_cabinet)).number if dev_cabinet else ''
        return context_data


class DeviceCreateView(SandboxCreateView):
    model = DeviceInfo
    form_class = DeviceCreateForm

    def get_context_data(self, **kwargs):
        public_data = get_device_public()
        kwargs.update(public_data)
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


class SupplierView(LoginRequiredMixin, BreadcrumbMixin, TemplateView):
    template_name = 'cmdb/supplier.html'


class SupplierCreateView(SandboxCreateView):
    model = Supplier
    fields = '__all__'


class SupplierUpdateView(SandboxUpdateView):
    model = Supplier
    fields = '__all__'


class SupplierListView(SandboxListView):
    model = Supplier
    fields = ['id', 'firm', 'contact_details', 'desc']

    def get_filters(self):
        data = self.request.GET
        filters = {}
        if 'firm' in data and data['firm']:
            filters['firm__icontains'] = data['firm']
        if 'contact_details' in data and data['contact_details']:
            filters['contact_deatils__icontains'] = data['contact_details']
        return filters


class SupplierDeleteView(SandboxDeleteView):
    model = Supplier


class NetworkAssetView(LoginRequiredMixin, BreadcrumbMixin, TemplateView):
    template_name = 'cmdb/network_asset.html'


class NetworkAssetCreateView(SandboxCreateView):
    model = NetworkAsset
    form_class = NetworkAssetForm

    def get_context_data(self, **kwargs):
        kwargs['all_provider'] = Supplier.objects.all()
        return super().get_context_data(**kwargs)


class NetworkAssetUpdateView(SandboxUpdateView):
    model = NetworkAsset
    form_class = NetworkAssetForm

    def get_context_data(self, **kwargs):
        kwargs['all_provider'] = Supplier.objects.all()
        return super().get_context_data(**kwargs)


class NetworkAssetListView(SandboxListView):
    model = NetworkAsset
    fields = ['id', 'name', 'ip_address', 'management', 'provider__firm', 'memory', 'disk', 'buyDate', 'warrantyDate', 'state']

    def get_filters(self):
        data = self.request.GET
        filters = {}
        if 'name' in data and data['name']:
            filters['name__icontains'] = data['name']
        if 'ip_address' in data and data['ip_address']:
            filters['ip_address__icontains'] = data['ip_address']
        return filters
    def get_datatables_paginator(self, request):
        context_data = super().get_datatables_paginator(request)
        data = context_data['data']
        for asset in data:
            disk = asset['disk']
            memory = asset['memory']
            if disk:
                di = re.match('(.*)/(.*)', disk)
                di_used = int(di.group(1))
                di_total = int(di.group(2))
                di_percent = '{:.0%}'.format(di_used/di_total)
                asset['disk'] = {'disk': disk, 'percent': di_percent}
            if memory:
                me = re.match('(.*)/(.*)', memory)
                me_used = int(me.group(1))
                me_total = int(me.group(2))
                me_percent = '{:.0%}'.format(me_used / me_total)
                asset['memory'] = {'memory': memory, 'percent': me_percent}

        return context_data


class NetworkAssetDeleteView(SandboxDeleteView):
    model = NetworkAsset


class NatRuleView(LoginRequiredMixin, BreadcrumbMixin, TemplateView):
    template_name = 'cmdb/natrule.html'

    def get_context_data(self, **kwargs):
        kwargs['all_cabinet'] = Cabinet.objects.all()
        return super().get_context_data(**kwargs)


class NatRuleCreateView(SandboxCreateView):
    model = NatRule
    form_class = NatRuleForm

    def get_context_data(self, **kwargs):
        kwargs['all_cabinet'] = Cabinet.objects.all()
        return super().get_context_data(**kwargs)


class NatRuleUpdateView(SandboxUpdateView):
    model = NatRule
    form_class = NatRuleForm

    def get_context_data(self, **kwargs):
        kwargs['all_cabinet'] = Cabinet.objects.all()
        return super().get_context_data(**kwargs)


class NatRuleListView(SandboxListView):
    model = NatRule
    fields = ['id', 'internet_ip', 'src_port', 'lan_ip', 'dest_port', 'state', 'dev_cabinet__number', 'desc']

    def get_filters(self):
        data = self.request.GET
        filters = {}
        if 'internet_ip' in data and data['internet_ip']:
            filters['internet_ip__icontains'] = data['internet_ip']
        if 'src_port' in data and data['src_port']:
            filters['src_port'] = data['src_port']
        if 'lan_ip' in data and data['lan_ip']:
            filters['lan_ip__icontains'] = data['lan_ip']
        if 'dest_port' in data and data['dest_port']:
            filters['dest_port'] = data['dest_port']
        if 'dev_cabinet' in data and data['dev_cabinet']:
            filters['dev_cabinet'] = data['dev_cabinet']
        if 'desc' in data and data['desc']:
            filters['desc__icontains'] = data['desc']
        return filters


class NatRuleDeleteView(SandboxDeleteView):
    model = NatRule

# class DomainNameView(LoginRequiredMixin, BreadcrumbMixin, TemplateView):
#     template_name = 'cmdb/domainname.html'
#
#
# class DomainNameCreateView(SandboxCreateView):
#     model = DomainName
#     form_class = NetworkAssetCreateForm
#
#     def get_context_data(self, **kwargs):
#         kwargs['all_supplier'] = Supplier.objects.all()
#         return super().get_context_data(**kwargs)
#
#
# class DomainNameUpdateView(SandboxUpdateView):
#     model = NetworkAsset
#     form_class = NetworkAssetUpdateForm
#
#     def get_context_data(self, **kwargs):
#         kwargs['all_provider'] = Supplier.objects.all()
#         return super().get_context_data(**kwargs)
#
#
# class DomainNameListView(SandboxListView):
#     model = NetworkAsset
#     fields = ['id', 'domain', 'resolution_server', 'domain_provider', 'state', 'buyDate', 'warrantyDate', 'desc']
#
#     def get_filters(self):
#         data = self.request.GET
#         filters = {'dn_type': '1'}
#         if 'domain' in data and data['domain']:
#             filters['domain__icontains'] = data['domain']
#         if 'resolution_server' in data and data['resolution_server']:
#             filters['resolution_server'] = data['resolution_server']
#         if 'domain_provider' in data and data['domain_provider']:
#             filters['domain_provider'] = data['domain_provider']
#
#         return filters
#
#
# class DomainNameDeleteView(SandboxDeleteView):
#     model = DomainName
