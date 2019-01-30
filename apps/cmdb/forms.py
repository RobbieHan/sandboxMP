# @Time   : 2018/12/19 16:13
# @Author : RobbieHan
# @File   : forms.py

from django import forms

from .models import Code, DeviceInfo


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
            'buyDate': {'required': '请填写购买日期'},
            'warrantyDate': {'required': '请填写到保日期'}
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