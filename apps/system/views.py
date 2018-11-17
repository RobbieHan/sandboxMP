from django.views.generic import TemplateView

from .mixin import LoginRequiredMixin
from custom import BreadcrumbMixin


class SystemView(LoginRequiredMixin, BreadcrumbMixin, TemplateView):

    template_name = 'system/system_index.html'

