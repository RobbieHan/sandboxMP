# @Time   : 2018/12/19 16:13
# @Author : RobbieHan
# @File   : forms.py

import re

from django import forms

from .models import Code, DeviceInfo, ConnectionInfo, DeviceFile, NetworkAsset, NatRule


class CodeCreateForm(forms.ModelForm):
    class Meta:
        model = Code
        fields = '__all__'

        error_messages = {
            'key': {'required': 'key不能为空'},
            'value': {'required': 'value不能为空'}
        }

    def clean(self):
        cleaned_data = super(CodeCreateForm, self).clean()
        key = cleaned_data.get('key')
        value = cleaned_data.get('value')

        if Code.objects.filter(key=key).count():
            raise forms.ValidationError('key：{}已存在'.format(key))

        if Code.objects.filter(value=value).count():
            raise forms.ValidationError('value: {}已存在'.format(value))


class CodeUpdateForm(CodeCreateForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        key = cleaned_data.get('key')
        value = cleaned_data.get('value')

        if self.instance:
            matching_code = Code.objects.exclude(pk=self.instance.pk)
            if matching_code.filter(key=key).exists():
                msg = 'key：{} 已经存在'.format(key)
                raise forms.ValidationError(msg)
            if matching_code.filter(value=value).exists():
                msg = 'value：{} 已经存在'.format(value)
                raise forms.ValidationError(msg)


class DeviceCreateForm(forms.ModelForm):
    class Meta:
        model = DeviceInfo
        exclude = ['dev_connection']
        error_messages = {
            'hostname': {'required': '请填写设备地址'},
        }

    def clean(self):
        cleaned_data = super(DeviceCreateForm, self).clean()
        hostname = cleaned_data.get('hostname')

        if DeviceInfo.objects.filter(hostname=hostname).count():
            raise forms.ValidationError('设备地址：{}已存在'.format(hostname))


class DeviceUpdateForm(DeviceCreateForm):
    def clean(self):
        cleaned_data = self.cleaned_data
        hostname = cleaned_data.get('hostname')

        if self.instance:
            matching_device = DeviceInfo.objects.exclude(pk=self.instance.pk)
            if matching_device.filter(hostname=hostname).exists():
                raise forms.ValidationError('设备地址：{}已存在'.format(hostname))


class ConnectionInfoForm(forms.ModelForm):

    class Meta:
        model = ConnectionInfo
        fields = '__all__'

        error_messages = {
            'port': {'required': '端口不能为空'},
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        private_key = cleaned_data.get('private_key')
        auth_type = cleaned_data.get('auth_type')
        if len(username) == 0:
            raise forms.ValidationError('用户名不能为空！')
        if auth_type == 'password' and len(password) == 0:
            raise forms.ValidationError('认证类型为[密码]时，必须设置密码信息！')
        if auth_type == 'private_key' and len(private_key) == 0:
            raise forms.ValidationError('认证类型为[密钥]时，必须设置密钥信息！')


class DeviceFileUploadForm(forms.ModelForm):
    class Meta:
        model = DeviceFile
        fields = '__all__'


class NetworkAssetForm(forms.ModelForm):
    class Meta:
        model = NetworkAsset
        fields = '__all__'
        error_messages = {
            'name': {'required': '请填写网络资产名称'},
        }

    def clean(self):
        cleaned_data = super(NetworkAssetForm, self).clean()
        memory = cleaned_data.get('memory')
        disk = cleaned_data.get('disk')
        show_on_top = cleaned_data.get('show_on_top')
        # if NetworkAsset.objects.filter(ip_address=ip_address).count():
        #     raise forms.ValidationError('资产地址已存在：{}已存在'.format(ip_address))
        if memory:
            me = re.match('(.*)/(.*)', memory)
            if me:
                try:
                    int(me.group(1))
                    int(me.group(2))
                except Exception:
                    raise forms.ValidationError('内存使用量和总量为整数')
            else:
                raise forms.ValidationError('内存格式不对，格式为：5/16 (用量/总量)')
        if disk:
            di = re.match('(.*)/(.*)', disk)
            if di:
                try:
                    int(di.group(1))
                    int(di.group(2))
                except Exception:
                    raise forms.ValidationError('硬盘使用量和总量为整数')
            else:
                raise forms.ValidationError('硬盘格式不对，格式为：5/16 (用量/总量)')
        show_on_top_count = NetworkAsset.objects.filter(show_on_top=True).count()
        if show_on_top and show_on_top_count >= 5:
            raise forms.ValidationError('首页最多展示5个链接')




class NatRuleForm(forms.ModelForm):
    class Meta:
        model = NatRule
        fields = '__all__'
        error_messages = {
            'internet_ip': {'required': '请填写公网IP'},
            'src_port': {'required': '请填写公网端口'},
            'lan_ip': {'required': '请填写内网地址'},
            'dest_port': {'required': '请填写内网端口'}
        }

