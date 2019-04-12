import re

from django.views.generic import View
from django.shortcuts import render
from system.mixin import LoginRequiredMixin
from .models import Cabinet, Code, DeviceInfo, NetworkAsset


class CmdbView(LoginRequiredMixin, View):

    def get(self, request):
        ret = dict()
        cabinet_all = Cabinet.objects.all()
        operation_type_all = Code.objects.filter(parent__key='operation_type')
        # net_asset=list(NetworkAsset.objects.filter(show_on_top=True).values())
        cabinet_list = []
        cabinet_count = []
        for cabinet in cabinet_all:
            cabinet_list.append(cabinet.number)
            cabinet_count.append(
                DeviceInfo.objects.filter(dev_cabinet=cabinet.id).count()
            )
        operations = []
        for operation in operation_type_all:
            count = DeviceInfo.objects.filter(operation_type=operation.id).count()
            data = {
                'name': operation.value,
                'count': count
            }
            operations.append(data)

        # for asset in net_asset:
        #     disk = asset['disk']
        #     memory = asset['memory']
        #     if disk:
        #         di = re.match('(.*)/(.*)', disk)
        #         di_used = int(di.group(1))
        #         di_total = int(di.group(2))
        #         di_percent = '{:.0%}'.format(di_used / di_total)
        #         asset['disk'] = {'disk': disk, 'percent': di_percent}
        #     if memory:
        #         me = re.match('(.*)/(.*)', memory)
        #         me_used = int(me.group(1))
        #         me_total = int(me.group(2))
        #         me_percent = '{:.0%}'.format(me_used / me_total)
        #         asset['memory'] = {'memory': memory, 'percent': me_percent}
        ret['cabinet_list'] = cabinet_list
        ret['cabinet_count'] = cabinet_count
        ret['operations'] = operations
        # ret['net_asset'] = net_asset
        return render(request, 'cmdb/cmdb_index.html', ret)
