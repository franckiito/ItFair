from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index, name = "index"),
    path('login/iniciar', views.login_iniciar, name="iniciar"),
    path('login/cerrar',views.cerrar_session,name="cerrar_session"),
    path('cuidador/registrar', views.registrar, name="registrar"),
    path('perfil/', views.perfil, name="perfil"),
    path('perfil/editar/<int:id>', views.editar_cuidador, name = "editar_cuidador"),
    path('abuelos',views.abuelos, name = "abuelos"),
    path('abuelos/crear', views.crear_abuelo, name="crear_abuelo"),
    path('abuelos/editar/<int:id>', views.editar_abuelo, name = "editar_abuelo"),
    path('abuelos/editado/<int:id>', views.editado_abuelo, name = "editado_abuelo"),
    path('abuelos/eliminar/<int:id>', views.eliminar_abuelo, name = "eliminar_abuelo"),
    path('abuelos/save', views.crear_abuelo_save, name="crear_abuelo_save"),
    path('remedio/<int:id>', views.remedio, name = "remedio"),
    path('remedio/crear/<int:id>', views.crear_remedio, name = "crear_remedio"),
    path('remedio/creado/<int:id>', views.creado_remedio, name = "creado_remedio"),
    #path('remedio/editar/<int:id>', views.editar_remedio, name = "editar_remedio"),
    #path('remedio/eliminar/<int:id>', views.eliminar_remedio, name = "eliminar_remedio"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)