from django.urls import path
from django.views.generic import TemplateView

app_name = 'configuracion'

urlpatterns = [
    path('', TemplateView.as_view(template_name='configuracion/index.html'), name='index'),
]
