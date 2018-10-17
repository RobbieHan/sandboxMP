# @Time   : 2018/10/17 23:13
# @Author : RobbieHan
# @File   : forms.py

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(required=True, error_messages={"requeired": "请填写用户名"})
    password = forms.CharField(required=True, error_messages={"requeired": "请填写密码"})