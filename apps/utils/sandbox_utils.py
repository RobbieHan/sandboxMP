# @Time   : 2018/12/29 19:22
# @Author : RobbieHan
# @File   : sandbox_utils.py

import os

from django.conf import settings

import yaml
import logging
import nmap
import paramiko

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


class SandboxScan(ConfigFileMixin):

    def basic_scan(self):
        """
        Use ICMP discovery online hosts and return online hosts.
        """
        hosts = self.get_net_address()
        nm = nmap.PortScanner()
        nm.scan(hosts=hosts, arguments='-n -sP -PE')
        online_hosts = nm.all_hosts()
        return online_hosts

    def os_scan(self):
        """
        Get the system type by nmap scan and return hosts list with os type.
        """
        hosts = self.get_net_address()
        nm = nmap.PortScanner()
        nm.scan(hosts=hosts, arguments='-n sS -O')
        online_hosts = []
        for host in nm.all_hosts():
            try:
                os_type = nm[host]['osmatch'][0]['osclass'][0]['osfamily']
            except Exception:
                os_type = 'unknown'
            host_dict = {'host': host, 'os': os_type}
            online_hosts.append(host_dict)
        return online_hosts

    def get_net_address(self):
        """
        Return the hosts that will be used to scan.
        Subclasses can override this to return any hosts.`
        """
        hosts_list = super().get_net_address()
        hosts = ' '.join(str(i) for i in hosts_list)
        return hosts


class LoginExecution(ConfigFileMixin):

    def login_execution(self, auth_type='password', **kwargs):
        """
        Support two authentication modes: password or private_key, and auth_type default is password.
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            if auth_type == 'password':
                ssh.connect(
                    kwargs['hostname'],
                    kwargs['port'],
                    kwargs['username'],
                    kwargs['password'],
                    timeout=3,
                )
                kwargs['auth_type'] = 'password'
            elif auth_type == 'private_key':
                kwargs['auth_type'] = 'private_key'
                private_key = paramiko.RSAKey.from_private_key_file(kwargs['private_key'])
                ssh.connect(
                    kwargs['hostname'],
                    kwargs['port'],
                    kwargs['username'],
                    private_key,
                    timeout=3,
                )
            kwargs['status'] = 'succeed'
            kwargs['error_message'] = ''
            commands = self.get_commands()
            for key, value in commands.items():
                stdin, stdout, stderr = ssh.exec_command(value, timeout=5)
                result = str(stdout.read()).strip('b').strip("'").strip('\\n')
                kwargs[key] = result
        except Exception as e:
            msg = '%(exc)s hostname %(hostname)s' % {
                'exc': e,
                'hostname': kwargs['hostname']
            }
            error_logger.error(msg)
            kwargs['status'] = 'failed'
            kwargs['error_message'] = str(e)
        return kwargs

    def password_login_execution(self, **kwargs):
        """
        Login to the remote system with a password.
        Kwargs is a dict containing hostname, port, username and password.
        Example: kwargs = {'hostname': '172.16.3.101', 'port': 22, 'username': 'root', 'password': 'paw123'}
        """
        return self.login_execution(**kwargs)

    def private_key_login_execution(self, **kwargs):
        """
        Login to the remote system with a private_key.
        Kwargs is a dict containing hostname, port, username and private key.
        Example:kwargs = {'hostname': '172.16.3.101', 'port': 22, 'username': 'root', 'private_key': '/root/.ssh/id_rsa'}
        """
        return self.login_execution(auth_type='private_key', **kwargs)

    def get_auth_type(self):
        key = ['hosts', 'auth_type']
        return self.get_conf_content(*key)

    def get_ssh_username(self):
        key = ['hosts', 'ssh_username']
        return self.get_conf_content(*key)

    def get_ssh_port(self):
        key = ['hosts', 'ssh_port']
        return self.get_conf_content(*key)

    def get_ssh_password(self):
        key = ['hosts', 'ssh_password']
        return self.get_conf_content(*key)

    def get_ssh_private_key(self):
        key = ['hosts', 'ssh_private_key']
        return self.get_conf_content(*key)

    def get_email(self):
        key = ['hosts', 'email']
        return self.get_conf_content(*key)

    def get_send_email(self):
        key = ['hosts', 'send_email']
        return self.get_conf_content(*key)

    def get_scan_type(self):
        key = ['hosts', 'scan_type']
        return self.get_conf_content(*key)