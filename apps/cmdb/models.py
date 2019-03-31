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
    desc = models.CharField(max_length=100, blank=True, default='', verbose_name='备注')

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
    sys_hostname = models.CharField(max_length=150, blank=True, default='', verbose_name='主机名')
    mac_address = models.CharField(max_length=150, blank=True, default='', verbose_name='MAC地址')
    sn_number = models.CharField(max_length=150, blank=True, default='', verbose_name='SN号码')
    os_type = models.CharField(max_length=150, blank=True, default='', verbose_name='系统类型')
    device_type = models.CharField(max_length=150, blank=True, default='', verbose_name='设备类型')

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
    operation_type = models.IntegerField(blank=True, null=True, verbose_name='所属项目')
    config = models.CharField(max_length=80, blank=True, default='', verbose_name='配置信息')
    dev_cabinet = models.IntegerField(blank=True, null=True, verbose_name='机柜信息')
    dev_connection = models.IntegerField(blank=True, null=True, verbose_name='连接信息')
    buyDate = models.DateField(default=datetime.now, blank=True, null=True, verbose_name="购买日期")
    warrantyDate = models.DateField(default=datetime.now, blank=True, null=True, verbose_name="到保日期")
    desc = models.TextField(blank=True, default='', verbose_name='备注信息')
    changed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    history = HistoricalRecords(excluded_fields=['add_time', 'modify_time', 'parent'])

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


class Supplier(models.Model):
    firm = models.CharField(max_length=200, verbose_name='供应商')
    contact_details = models.CharField(max_length=200, verbose_name='联系信息')
    desc = models.CharField(max_length=200, blank=True, default='', verbose_name='备注信息')

    class Meta:
        verbose_name = '供应商管理'
        verbose_name_plural = verbose_name


class NetworkAsset(models.Model):
    name = models.CharField(max_length=100, verbose_name='资产名称')
    ip_address = models.CharField(max_length=100, blank=True, default='', verbose_name='IP地址')
    management = models.CharField(max_length=100, blank=True, default='', verbose_name='管理地址')
    show_on_top = models.BooleanField(default=False, verbose_name='首页展示')
    provider = models.ForeignKey('Supplier', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='服务商')
    desc = models.TextField(blank=True, default='', verbose_name='备注信息')

    class Meta:
        verbose_name = '网络资产'
        verbose_name_plural = verbose_name


class DomainName(AbstractMode):
    dn_type_choices = (('1', '主域名'),('2', '二级域名'))
    domain = models.CharField(max_length=200, verbose_name='域名')
    dn_type = models.CharField(max_length=20, choices=dn_type_choices, default='1')
    addr_resolution = models.ForeignKey('NatRule', blank=True, null=True,
                                        on_delete=models.SET_NULL, verbose_name='解析地址')
    resolution_server = models.ForeignKey('Supplier', related_name='res_server',
                                          blank=True, null=True, on_delete=models.SET_NULL, verbose_name='解析服务')
    domain_provider = models.ForeignKey('Supplier', related_name='do_provider',
                                        blank=True, null=True, on_delete=models.SET_NULL, verbose_name='解析服务')
    state = models.BooleanField(default=True, verbose_name='状态')
    ssl = models.FileField(upload_to="ssl_file/%Y/%m", null=True, blank=True, verbose_name="SSL证书")
    buyDate = models.DateField(default=datetime.now, blank=True, null=True, verbose_name='购买日期')
    warrantyDate = models.DateField(default=datetime.now, blank=True, null=True, verbose_name='到保日期')
    desc = models.TextField(blank=True, default='', verbose_name='备注信息')

    class Meta:
        verbose_name = '域名管理'
        verbose_name_plural = verbose_name


class NatRule(models.Model):
    internet_ip = models.CharField(max_length=80, blank=True, default='', verbose_name='互联网IP')
    src_port = models.IntegerField(blank=True, default='', verbose_name='源端口')
    lan_ip = models.CharField(max_length=80, blank=True, default='', verbose_name='内网IP')
    dest_port = models.IntegerField(blank=True, default='', verbose_name='目的端口')
    state = models.BooleanField(default=True, verbose_name='状态')
    desc = models.TextField(blank=True, default='', verbose_name='备注信息')

    class Meta:
        verbose_name = 'NAT规则'
        verbose_name_plural = verbose_name