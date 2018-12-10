from django.views.generic import TemplateView

from system.mixin import LoginRequiredMixin
from custom import BreadcrumbMixin


class CmdbView(LoginRequiredMixin, BreadcrumbMixin, TemplateView):

    template_name = 'cmdb/cmdb_index.html'
