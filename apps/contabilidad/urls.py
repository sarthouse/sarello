from django.urls import path
from . import views

app_name = 'contabilidad'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('plan-cuentas/', views.plan_cuentas, name='plan_cuentas'),
    path('cuenta/crear/', views.cuenta_create, name='cuenta_create'),
    path('cuenta/<int:pk>/', views.cuenta_detail, name='cuenta_detail'),
    path('cuenta/<int:pk>/editar/', views.cuenta_edit, name='cuenta_edit'),
    path('cuenta/<int:pk>/eliminar/', views.cuenta_delete, name='cuenta_delete'),
    path('ejercicio/crear/', views.ejercicio_create, name='ejercicio_create'),
    path('ejercicio/<int:pk>/editar/', views.ejercicio_edit, name='ejercicio_edit'),
    path('asientos/', views.lista_asientos, name='asientos'),
    path('asiento/crear/', views.asiento_create, name='asiento_create'),
    path('asiento/<int:pk>/', views.asiento_detail, name='asiento_detail'),
    path('asiento/<int:pk>/editar/', views.asiento_edit, name='asiento_edit'),
    path('asiento/<int:pk>/eliminar/', views.asiento_delete, name='asiento_delete'),
    path('asiento/<int:pk>/linea/', views.asiento_agregar_linea, name='asiento_agregar_linea'),
    path('asiento/<int:pk>/linea/<int:linea_id>/eliminar/', views.asiento_eliminar_linea, name='asiento_eliminar_linea'),
    path('libro-diario/', views.libro_diario, name='libro_diario'),
    path('mayor/', views.mayor, name='mayor'),
    path('balance/', views.balance, name='balance'),
    path('estado-resultados/', views.estado_resultados, name='estado_resultados'),
    path('cuentas/importar/', views.importar_cuentas, name='importar_cuentas'),
    path('cuentas/importar/confirmar/', views.importar_cuentas_confirmar, name='importar_cuentas_confirmar'),
    path('cuentas/importar/guia/', views.descargar_guia_csv, name='descargar_guia'),
    path('cuentas/bulk/delete/', views.cuentas_bulk_delete, name='cuentas_bulk_delete'),
    path('cuenta/<int:pk>/toggle/', views.cuenta_toggle_active, name='cuenta_toggle'),
    path('ejercicio/<int:pk>/preview-cierre/', views.preview_cierre, name='preview_cierre'),
    path('ejercicio/<int:pk>/cerrar/', views.cerrar_ejercicio, name='cerrar_ejercicio'),
    path('ejercicio/<int:pk>/apertura/', views.generar_apertura, name='generar_apertura'),
]
