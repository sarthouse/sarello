from django.urls import path
from . import views

app_name = 'contactos'

urlpatterns = [
    path('', views.index, name='index'),
    path('lista/', views.lista, name='lista'),
    path('crear/', views.contacto_create, name='contacto_create'),
    path('<int:pk>/', views.contacto_detail, name='contacto_detail'),
    path('<int:pk>/editar/', views.contacto_edit, name='contacto_edit'),
    path('<int:pk>/eliminar/', views.contacto_delete, name='contacto_delete'),
]
