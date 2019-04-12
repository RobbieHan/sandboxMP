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

    path('eam/device/', views_eam.DeviceView.as_view(), name='eam-device'),
    path('eam/device/create/', views_eam.DeviceCreateView.as_view(), name='eam-device-create'),
    path('eam/device/update/', views_eam.DeviceUpdateView.as_view(), name='eam-device-update'),
    path('eam/device/list/', views_eam.DeviceListView.as_view(), name='eam-device-list'),
    path('eam/device/delete/', views_eam.DeviceDeleteView.as_view(), name='eam-device-delete'),
    path('eam/device/device2connection/', views_eam.Device2ConnectionView.as_view(), name='eam-device-device2connection'),
    path('eam/device/detail/', views_eam.DeviceDetailView.as_view(), name='eam-device-detail'),
    path('eam/device/upload/', views_eam.DeviceFileUploadView.as_view(), name='eam-device-upload'),
    path('eam/device/file_delete/', views_eam.DeviceFileDeleteView.as_view(), name='eam-device-file_delete'),
    path('eam/device/auto_update_device_info/', views_eam.AutoUpdateDeviceInfo.as_view(),
         name='eam-device-auto_update_device_info'),

    path('eam/supplier/', views_eam.SupplierView.as_view(), name='eam-supplier'),
    path('eam/supplier/create/', views_eam.SupplierCreateView.as_view(), name='eam-supplier-create'),
    path('eam/supplier/update/', views_eam.SupplierUpdateView.as_view(), name='eam-supplier-update'),
    path('eam/supplier/list/', views_eam.SupplierListView.as_view(), name='eam-supplier-list'),
    path('eam/supplier/delete/', views_eam.SupplierDeleteView.as_view(), name='eam-supplier-delete'),

    path('eam/network_asset/', views_eam.NetworkAssetView.as_view(), name='eam-network_asset'),
    path('eam/network_asset/create/', views_eam.NetworkAssetCreateView.as_view(), name='eam-network_asset-create'),
    path('eam/network_asset/update/', views_eam.NetworkAssetUpdateView.as_view(), name='eam-network_asset-update'),
    path('eam/network_asset/list/', views_eam.NetworkAssetListView.as_view(), name='eam-network_asset-list'),
    path('eam/network_asset/delete/', views_eam.NetworkAssetDeleteView.as_view(), name='eam-network_asset-delete'),

    path('eam/natrule/', views_eam.NatRuleView.as_view(), name='eam-natrule'),
    path('eam/natrule/create/', views_eam.NatRuleCreateView.as_view(), name='eam-natrule-create'),
    path('eam/natrule/update/', views_eam.NatRuleUpdateView.as_view(), name='eam-natrule-update'),
    path('eam/natrule/list/', views_eam.NatRuleListView.as_view(), name='eam-natrule-list'),
    path('eam/natrule/delete/', views_eam.NatRuleDeleteView.as_view(), name='eam-natrule-delete'),

    path('eam/domain/', views_eam.DomainNameView.as_view(), name='eam-domain'),
    path('eam/domain/create/', views_eam.DomainNameCreateView.as_view(), name='eam-domain-create'),
    path('eam/domain/update/', views_eam.DomainNameUpdateView.as_view(), name='eam-domain-update'),
    path('eam/domain/list/', views_eam.DomainNameListView.as_view(), name='eam-domain-list'),
    path('eam/domain/delete/', views_eam.DomainNameDeleteView.as_view(), name='eam-domain-delete'),
    path('eam/domain/dn2nr/', views_eam.DomainName2NatRule.as_view(), name='eam-domain-dn2nr'),
]
