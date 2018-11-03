from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index, name = "index"),
    path('cuidador/registrar', views.registrar, name="registrar"),
    path('abuelos',views.abuelos, name = "abuelos"),
    path('abuelos/crear', views.crear_abuelo, name="crear_abuelo"),
    path('abuelos/save', views.crear_abuelo_save, name="crear_abuelo_save")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)