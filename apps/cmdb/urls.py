from django.urls import path

from .views import CmdbView
from . import views_code, views_scan, views_eam

app_name = 'cmdb'

urlpatterns = [
    path('', CmdbView.as_view(), name='index'),
    path('portal/code/', views_code.CodeView.as_view(), name='portal-code'),
    path('portal/code/create/', views_code.CodeCreateView.as_view(), name='portal-code-create'),
    path('portal/code/list/', views_code.CodeListView.as_view(), name='portal-code-list'),
    path('portal/code/update/', views_code.CodeUpdateView.as_view(), name='portal-code-update'),
    path('portal/code/delete/', views_code.CodeDeleteView.as_view(), name='portal-code-delete'),

    path('portal/scan_config/', views_scan.ScanConfigView.as_view(), name='portal-scan_config'),
    path('portal/device_scan/', views_scan.DeviceScanView.as_view(), name='portal-device_scan'),
    path('portal/device_scan/list/', views_scan.DeviceScanListView.as_view(), name='portal-device_scan-list'),
    path('portal/device_scan/detail/', views_scan.DeviceScanDetailView.as_view(), name='portal-device_scan-detail'),
    path('portal/device_scan/delete/', views_scan.DeviceScanDeleteView.as_view(), name='portal-device_scan-delete'),
    path('portal/device_scan/exec/', views_scan.DeviceScanExecView.as_view(), name='portal-device_scan-exec'),
    path('portal/device_scan/inbound/', views_scan.DeviceScanInboundView.as_view(), name='portal-device_scan-inbound'),

    path('eam/cabinet/', views_eam.CabinetView.as_view(), name='eam-cabinet'),
    path('eam/cabinet/create/', views_eam.CabinetCreateView.as_view(), name='eam-cabinet-create'),
    path('eam/cabinet/update/', views_eam.CabinetUpdateView.as_view(), name='eam-cabinet-update'),
    path('eam/cabinet/list/', views_eam.CabinetListView.as_view(), name='eam-cabinet-list'),
    path('eam/cabinet/delete/', views_eam.CabinetDeleteView.as_view(), name='eam-cabinet-delete'),

]
