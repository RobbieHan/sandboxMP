# @Time   : 2018/12/29 19:25
# @Author : RobbieHan
# @File   : views_scan.py

import ast
import logging
from ruamel import yaml

from django.views.generic import View, TemplateView
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from celery_once import AlreadyQueued

from system.mixin import LoginRequiredMixin
from custom import BreadcrumbMixin, SandboxListView, SandboxDeleteView
from utils.sandbox_utils import ConfigFileMixin
from system.models import Menu
from .models import (DeviceScanInfo, ConnectionInfo, DeviceInfo,
                     ConnectionAbstract, DeviceAbstract)
from .tasks import scan_execution

error_logger = logging.getLogger('sandbox_error')


class ScanConfigView(LoginRequiredMixin, BreadcrumbMixin, ConfigFileMixin, View):

    def get(self, request):
        menu = Menu.get_menu_by_request_url(request.path_info)
        template_name = 'cmdb/scan_config.html'
        context = self.get_conf_content()
        context.update(menu)
        return render(request, template_name, context)

    def post(self, request):
        ret = dict(result=False)
        config = dict()
        hosts = request.POST
        try:
            config['net_address'] = ast.literal_eval(hosts['net_address'])
            config['ssh_username'] = hosts['ssh_username']
            config['ssh_port'] = hosts['ssh_port']
            config['ssh_password'] = hosts['ssh_password']
            config['ssh_private_key'] = hosts['ssh_private_key']
            config['commands'] = ast.literal_eval(hosts['commands'])
            config['auth_type'] = hosts['auth_type']
            config['scan_type'] = hosts['scan_type']
            config['email'] = hosts['email']
            config['send_email'] = hosts['send_email']
            data = dict(hosts=config)
            config_file = self.get_config_file()
            with open(config_file, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, Dumper=yaml.RoundTripDumper, indent=4)
                ret['result'] = True
        except Exception as e:
            error_logger.error(e)

        return JsonResponse(ret)


class DeviceScanView(LoginRequiredMixin, BreadcrumbMixin, TemplateView):
    template_name = 'cmdb/device_scan.html'


class DeviceScanListView(SandboxListView):
    model = DeviceScanInfo
    fields = ['id', 'sys_hostname', 'hostname', 'mac_address', 'auth_type', 'status', 'os_type', 'device_type']


class DeviceScanDetailView(LoginRequiredMixin, View):

    def get(self, request):
        ret = Menu.get_menu_by_request_url(request.path_info)
        if 'id' in request.GET and request.GET['id']:
            device = get_object_or_404(DeviceScanInfo, pk=int(request.GET['id']))
            ret['device'] = device
        return render(request, 'cmdb/device_scan_detail.html', ret)


class DeviceScanDeleteView(SandboxDeleteView):
    model = DeviceScanInfo


class DeviceScanExecView(LoginRequiredMixin, View):

    def get(self, request):
        ret = dict(status='fail')
        try:
            scan_execution.delay()
            ret['status'] = 'success'
        except AlreadyQueued:
            ret['status'] = 'already_queued'
        return JsonResponse(ret)


class DeviceScanInboundView(LoginRequiredMixin, View):
    def post(self, request):
        ret = dict(result=False)
        login_succeed = list(DeviceScanInfo.objects.filter(status='succeed').values())
        connection_fields = [field.name for field in ConnectionAbstract._meta.fields if field.name is not 'id']
        device_fields = [field.name for field in DeviceAbstract._meta.fields if field.name is not 'id']
        device_fields.append('hostname')
        for host in login_succeed:
            connection_defaults = {key: host[key] for key in host.keys() & connection_fields}
            device_defaults = {key: host[key] for key in host.keys() & device_fields}
            connection_info, _ = ConnectionInfo.objects.update_or_create(
                hostname=host['hostname'],
                defaults=connection_defaults
            )
            connection_id = int(getattr(connection_info, 'id'))
            device_defaults['dev_connection'] = connection_id
            device_defaults['changed_by_id'] = request.user.id
            DeviceInfo.objects.update_or_create(
                hostname=host['hostname'],
                defaults=device_defaults
            )
        ret['result'] = True
        return JsonResponse(ret)
