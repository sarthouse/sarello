from django.urls import path
from . import views

app_name = 'tesoreria'

urlpatterns = [
    path('', views.index, name='index'),
    path('cuentas/', views.cuentas, name='cuentas'),
    path('cuentas/crear/', views.cuenta_create, name='cuenta_create'),
    path('cuentas/<int:pk>/editar/', views.cuenta_edit, name='cuenta_edit'),
    path('cuentas/<int:pk>/eliminar/', views.cuenta_delete, name='cuenta_delete'),
    path('movimientos/', views.movimientos, name='movimientos'),
    path('movimientos/crear/', views.movimiento_create, name='movimiento_create'),
    path('movimientos/<int:pk>/', views.movimiento_detail, name='movimiento_detail'),
    path('movimientos/<int:pk>/editar/', views.movimiento_edit, name='movimiento_edit'),
    path('movimientos/<int:pk>/anular/', views.movimiento_anular, name='movimiento_anular'),
    path('movimientos/<int:pk>/eliminar/', views.movimiento_delete, name='movimiento_delete'),
    path('caja-diaria/', views.caja_diaria, name='caja_diaria'),
    path('saldos/', views.saldo_cuentas, name='saldo_cuentas'),
    path('conciliar/', views.conciliar_cuentas, name='conciliar'),
]
