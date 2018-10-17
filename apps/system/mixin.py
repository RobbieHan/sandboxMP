# @Time   : 2018/10/17 15:15
# @Author : RobbieHan
# @File   : mixin.py.py

from django.contrib.auth.decorators import login_required


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **init_kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**init_kwargs)
        return login_required(view)