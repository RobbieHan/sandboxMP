# @Time   : 2018/12/29 19:22
# @Author : RobbieHan
# @File   : sandbox_utils.py

import os

from django.conf import settings

import yaml
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sandboxMP.settings')
error_logger = logging.getLogger('sandbox_error')


class ConfigFileMixin:
    config_file = None

    def get_config_file(self):
        """
        Return 'config_file' that will be used to look up the scan hosts IP,
        network, range of IP, or other config settings.
        This method is called by the default implementation of get_hosts(),
        """

        if self.config_file is None:
            config_file = os.path.join(os.path.join(settings.BASE_DIR, 'config'), 'scanhosts.yml')
            if os.path.exists(config_file):
                return config_file
            else:
                msg = ' %(cls)s is missing a config file. Define %(cls)s.config_file, ' \
                      'or override %(cls)s.get_config_file().' % {'cls': self.__class__.__name__}
                error_logger.error(msg)
                raise ValueError(msg)

        return self.config_file

    def get_conf_content(self, *key):
        """
        Get the configuration content from config file .
        Example ssh_password, commands, email which is in the config file.
        """
        _config = self.get_config_file()
        with open(_config) as f:
            content = yaml.load(f)
        if key is not None:
            try:
                num = 0
                while num < len(key):
                    content = content[key[num]]
                    num += 1
            except Exception as e:
                msg = '%(exc)s is not in %(config)s.' % {
                    'exc': e,
                    'config': _config
                }
                error_logger.error(msg)
                raise ValueError(msg)
        return content

    def get_commands(self):
        """
        Get the commands from config file.
        """
        key = ['hosts', 'commands']
        return self.get_conf_content(*key)

    def get_net_address(self):
        """
        Return the hosts that will be used to scan.
        Subclasses can override this to return any hosts.
        """
        key = ['hosts', 'net_address']
        return self.get_conf_content(*key)
