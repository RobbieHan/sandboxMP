from django.urls import path

from .views import SystemView
from . import views_structure

app_name = 'system'

urlpatterns = [
    path('', SystemView.as_view(), name='login'),
    path('basic/structure/', views_structure.StructureView.as_view(), name='basic-structure'),
    path('basic/structure/create/', views_structure.StructureCreateView.as_view(), name='basic-structure-create'),
    path('basic/structure/list/', views_structure.StructureListView.as_view(), name='basic-structure-list'),
]

