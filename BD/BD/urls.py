"""BD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Index, name='inicio'),
    path('login/', views.Login, name='login'),
    path('registrarse/', views.Registrarse, name='registrarse'),
    path('menu-admin/', views.MenuAdmin, name='menu_admin'),
    path('crear-rol-usuario/', views.CrearRolUsuario, name='crear_rol_usuario'),
    path('crear-rol-grupo/', views.CrearRolGrupo, name='crear_rol_grupo'),
    path('menu-crear-usuario/', views.MenuCrearUsuario, name='menu_crear_usuario'),
    path('crear-usuario-grupo/', views.CrearUsuarioGrupo,
         name='crear_usuario_grupo'),
    path('crear-usuario-singular/', views.CrearUsuarioSingular,
         name='crear_usuario_singular'),
    path('ver-rol/', views.VerRol, name='ver_rol'),
    path('ver-usuario/', views.VerUsuario, name='ver_usuario'),
    path('crear-permiso/', views.CrearPermisos, name='crear_permiso'),
]
