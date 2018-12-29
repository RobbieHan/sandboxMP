# @Time   : 2018/12/29 19:25
# @Author : RobbieHan
# @File   : views_scan.py

import ast
import logging
from ruamel import yaml

from django.views.generic import View
from django.http import JsonResponse
from django.shortcuts import render


from system.mixin import LoginRequiredMixin
from custom import BreadcrumbMixin
from utils.sandbox_utils import ConfigFileMixin
from system.models import Menu

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
