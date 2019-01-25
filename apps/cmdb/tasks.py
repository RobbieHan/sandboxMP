import time
import logging

from celery import shared_task
from celery_once import QueueOnce

from utils.sandbox_utils import SandboxScan, LoginExecution
from .models import DeviceScanInfo

info_logger = logging.getLogger('sandbox_info')


@shared_task(base=QueueOnce)
def scan_execution():
    scan = SandboxScan()
    execution = LoginExecution()
    scan_type = execution.get_scan_type()
    auth_type = execution.get_auth_type()
    start_time = time.time()
    if scan_type == 'basic_scan':
        hosts = scan.basic_scan()
        for host in hosts:
            DeviceScanInfo.objects.update_or_create(
                hostname=host,
            )
    else:
        hosts = scan.os_scan()
        login_hosts = [host for host in hosts if host['os'] in ['Linux', 'embedded']]
        nologin_hosts = [host for host in hosts if host not in login_hosts]
        for host in nologin_hosts:
            DeviceScanInfo.objects.update_or_create(
                hostname=host['host'],
                defaults={
                    'os_type': host['os']
                }
            )
        for host in login_hosts:
            kwargs = {
                'hostname': host['host'],
                'username': execution.get_ssh_username(),
                'port': execution.get_ssh_port(),
                'password': execution.get_ssh_password(),
                'private_key': execution.get_ssh_private_key()
            }
            defaults = execution.login_execution(auth_type=auth_type, **kwargs)
            DeviceScanInfo.objects.update_or_create(
                hostname=host['host'],
                defaults=defaults
            )
    end_time = time.time()
    msg = 'Scan task has been completed, execution time: %(time)s, %(num)s hosts are up.' % {
        'time': end_time - start_time,
        'num': len(hosts)
    }
    info_logger.info(msg)
    return msg