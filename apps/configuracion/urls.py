from django.urls import path
from . import views

app_name = 'configuracion'

urlpatterns = [
    path('', views.index, name='index'),
    path('parametros/', views.parametros, name='parametros'),
    path('parametros/<int:pk>/editar/', views.parametro_edit, name='parametro_edit'),
    path('datos-empresa/', views.datos_empresa, name='datos_empresa'),
]
