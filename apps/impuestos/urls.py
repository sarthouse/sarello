from django.urls import path
from . import views

app_name = 'impuestos'

urlpatterns = [
    path('', views.index, name='index'),
    path('tipos/', views.tipos, name='tipos'),
    path('tipos/crear/', views.tipo_create, name='tipo_create'),
    path('tipos/<int:pk>/editar/', views.tipo_edit, name='tipo_edit'),
    path('tipos/<int:pk>/eliminar/', views.tipo_delete, name='tipo_delete'),
    path('alicuotas/', views.alicuotas, name='alicuotas'),
    path('alicuotas/crear/', views.alicuota_create, name='alicuota_create'),
    path('alicuotas/<int:pk>/editar/', views.alicuota_edit, name='alicuota_edit'),
    path('alicuotas/<int:pk>/eliminar/', views.alicuota_delete, name='alicuota_delete'),
]
