from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index, name = "index"),
    path('login/iniciar', views.login_iniciar, name="iniciar"),
    path('login/cerrar',views.cerrar_session,name="cerrar_session"),
    path('cuidador/registrar', views.registrar, name="registrar"),
    path('abuelos',views.abuelos, name = "abuelos"),
    path('abuelos/crear', views.crear_abuelo, name="crear_abuelo")
]