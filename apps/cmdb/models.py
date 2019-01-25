from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

from simple_history.models import HistoricalRecords

User = get_user_model()


class AbstractMode(models.Model):
    parent = models.ForeignKey(
        'self', blank=True, null=True, on_delete=models.SET_NULL, related_name='child'
    )

    class Meta:
        abstract = True


class Code(AbstractMode):
    key = models.CharField(max_length=80, verbose_name='键')
    value = models.CharField(max_length=80, verbose_name='值')
    desc = models.BooleanField(default=True, verbose_name='备注')

    class Meta:
        verbose_name = '字典'
        verbose_name_plural = verbose_name


class TimeAbstract(models.Model):
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    modify_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        abstract = True


class ConnectionAbstract(models.Model):
    auth_method_choices = (
        ('private_key', '密钥认证'),
        ('password', '密码认证')
    )
    hostname = models.CharField(max_length=50, verbose_name='设备地址(IP或域名)')
    port = models.IntegerField(default=22, verbose_name='SSH端口')
    username = models.CharField(max_length=15, blank=True, default='', verbose_name='SSH用户名')
    password = models.CharField(max_length=80, blank=True, default='', verbose_name='SSH密码')
    private_key = models.CharField(max_length=100, blank=True, default='', verbose_name='密钥路径')
    auth_type = models.CharField(max_length=30, choices=auth_method_choices, default='')
    status = models.CharField(max_length=10, blank=True, default='')

    class Meta:
        abstract = True


class DeviceAbstract(models.Model):
    sys_hostname = models.CharField(max_length=50, blank=True, default='', verbose_name='主机名')
    mac_address = models.CharField(max_length=50, blank=True, default='', verbose_name='MAC地址')
    sn_number = models.CharField(max_length=50, blank=True, default='', verbose_name='SN号码')
    os_type = models.CharField(max_length=50, blank=True, default='', verbose_name='系统类型')
    device_type = models.CharField(max_length=50, blank=True, default='', verbose_name='设备类型')

    class Meta:
        abstract = True


class DeviceScanInfo(ConnectionAbstract, DeviceAbstract, TimeAbstract):
    error_message = models.CharField(max_length=80, blank=True, default='', verbose_name='错误信息')

    class Meta:
        verbose_name = '扫描信息'
        verbose_name_plural = verbose_name


class ConnectionInfo(ConnectionAbstract, TimeAbstract):

    class Meta:
        verbose_name = 'SSH连接信息'
        verbose_name_plural = verbose_name


class Cabinet(models.Model):
    number = models.CharField(max_length=50, verbose_name='机柜编号')
    position = models.CharField(max_length=80, verbose_name='机柜位置')
    desc = models.TextField(blank=True, default='', verbose_name='备注信息')

    class Meta:
        verbose_name = '机柜信息'
        verbose_name_plural = verbose_name


class DeviceInfo(AbstractMode, DeviceAbstract, TimeAbstract):
    hostname = models.CharField(max_length=50, verbose_name='设备地址(IP或域名)')
    network_type = models.IntegerField(blank=True, null=True, verbose_name='网络类型')
    service_type = models.IntegerField(blank=True, null=True, verbose_name='服务类型')
    operation_type = models.IntegerField(blank=True, null=True, verbose_name='业务类型')
    leader = models.IntegerField(blank=True, null=True, verbose_name='责任人')
    dev_cabinet = models.IntegerField(blank=True, null=True, verbose_name='机柜信息')
    dev_connection = models.IntegerField(blank=True, null=True, verbose_name='连接信息')
    buyDate = models.DateField(default=datetime.now, verbose_name="购买日期")
    warrantyDate = models.DateField(default=datetime.now, verbose_name="到保日期")
    desc = models.TextField(blank=True, default='', verbose_name='备注信息')
    changed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    history = HistoricalRecords(excluded_fields=['add_time', 'modify_time'])

    class Meta:
        verbose_name = '设备信息'
        verbose_name_plural = verbose_name

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value


class DeviceFile(TimeAbstract):
    device = models.ForeignKey('DeviceInfo', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='设备')
    file_content = models.FileField(upload_to="asset_file/%Y/%m", null=True, blank=True, verbose_name="资产文件")
    upload_user = models.CharField(max_length=20, verbose_name="上传人")

