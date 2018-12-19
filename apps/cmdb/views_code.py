# @Time   : 2018/12/19 13:31
# @Author : RobbieHan
# @File   : views_code.py.py

from django.views.generic import TemplateView

from system.mixin import LoginRequiredMixin
from custom import (BreadcrumbMixin, SandboxCreateView,
                    SandboxListView, SandboxUpdateView, SandboxDeleteView)
from .models import Code
from .forms import CodeCreateForm, CodeUpdateForm


class CodeView(LoginRequiredMixin, BreadcrumbMixin, TemplateView):
    template_name = 'cmdb/code.html'

    def get_context_data(self):
        context = dict(code_parent=Code.objects.filter(parent=None))
        return context


class CodeCreateView(SandboxCreateView):
    model = Code
    form_class = CodeCreateForm
    template_name_suffix = '_create'

    def get_context_data(self, **kwargs):
        kwargs['code_parent'] = Code.objects.filter(parent=None)
        return super().get_context_data(**kwargs)


class CodeListView(SandboxListView):
    model = Code
    fields = ['id', 'key', 'value', 'parent__value']

    def get(self, request):
        if 'parent' in request.GET and request.GET['parent']:
            self.filters = dict(parent__key=request.GET['parent'])
        return super().get(request)


class CodeUpdateView(SandboxUpdateView):
    model = Code
    form_class = CodeUpdateForm
    template_name_suffix = '_update'

    def get_context_data(self, **kwargs):
        kwargs['code_parent'] = Code.objects.filter(parent=None)
        return super().get_context_data(**kwargs)


class CodeDeleteView(SandboxDeleteView):
    model = Code
