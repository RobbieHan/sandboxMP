from django.test import TestCase

# Create your tests here.
from django.views.generic.base import View
from django.shortcuts import HttpResponse
import logging
from .models import Code

info_logger = logging.getLogger('sandbox_info')
error_logger = logging.getLogger('sandbox_error')


class TestLoggingView(View):

    def get(self, request):
        print('a')
        info_logger.info('The system print a letter "a" ')
        try:
            Code.objects.get(id=100)
        except Exception as e:
            error_logger.error(e)
        return HttpResponse("OK!")