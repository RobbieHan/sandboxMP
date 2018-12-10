from django.urls import path

from .views import CmdbView

app_name = 'cmdb'

urlpatterns = [
    path('', CmdbView.as_view(), name='index'),
]
