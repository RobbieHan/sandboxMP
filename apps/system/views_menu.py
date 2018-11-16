from django.views.generic import ListView

from .mixin import LoginRequiredMixin
from apps.custom import SandboxCreateView, SandboxUpdateView, BreadcrumbMixin
from .models import Menu


class MenuCreateView(SandboxCreateView):
    model = Menu
    fields = '__all__'

    def get_context_data(self, **kwargs):
        kwargs['menu_all'] = Menu.objects.all()
        return super().get_context_data(**kwargs)


class MenuListView(LoginRequiredMixin, BreadcrumbMixin, ListView):
    model = Menu
    context_object_name = 'menu_all'


class MenuUpdateView(SandboxUpdateView):
    model = Menu
    fields = '__all__'
    template_name_suffix = '_update'

    def get_context_data(self, **kwargs):
        kwargs['menu_all'] = Menu.objects.all()
        return super().get_context_data(**kwargs)
