from django.urls import path

from .views import SystemView

app_name = 'system'

urlpatterns = [
    path('', SystemView.as_view(), name='login'),
]
