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
    path('salir/', views.Salir, name='salir'),
    path('registrarse/', views.Registrarse, name='registrarse'),
    path('crear-rol-usuario/', views.CrearRolUsuario, name='crear_rol_usuario'),
    path('crear-rol-grupo/', views.CrearRolGrupo, name='crear_rol_grupo'),
    path('menu-crear-usuario/', views.MenuCrearUsuario, name='menu_crear_usuario'),
    path('crear-usuario-grupo/', views.CrearUsuarioGrupo,
         name='crear_usuario_grupo'),
    path('crear-usuario-singular/', views.CrearUsuarioSingular,
         name='crear_usuario_singular'),
    path('ver-rol/', views.VerRol, name='ver_rol'),
    path('ver-rol-grupo/', views.VerRolGrupo, name='ver_rol_grupo'),
    path('ver-rol-singular/', views.VerRolSingular, name='ver_rol_singular'),
    path('ver-rol-todos/', views.VerRolesTodos, name='ver_rol_todos'),
    path('ver-usuario/', views.VerUsuario, name='ver_usuario'),
    path('ver-usuario-grupo/', views.VerUsuarioGrupo, name='ver_usuario_grupo'),
    path('ver-usuario-singular/', views.VerUsuarioSingular,
         name='ver_usuario_singular'),
    path('ver-usuario-todos/', views.VerUsuarioTodos, name='ver_usuario_todos'),
    path('crear-permiso/', views.CrearPermisos, name='crear_permiso'),
    path('crear-proveedor/', views.CrearProveedor, name='crear_proveedor'),
    path('crear-cuenta-bancaria/', views.CrearCuentaBancaria, name='crear_cuenta_bancaria'),
    path('crear-chequera/', views.CrearChequera, name='crear_chequera'),
    path('registrar-deposito/', views.RegistrarDeposito, name='registrar_deposito'),
    path('ver-deposito/', views.VerDeposito, name='ver_deposito'),
    path('ver-chequera/', views.VerChequera, name='ver_chequera'),
    path('ver-chequera-todos/', views.VerChequeraTodos, name='ver_chequera_todos'),
    path('ver-chequera-alerta/', views.VerChequeraAlerta,
         name='ver_chequera_alerta'),
    path('ver-chequera-agotado/', views.VerChequeraAgotado,
         name='ver_chequera_agotado'),
    path('ver-chequera-disponible/', views.VerChequeraDisponible,
         name='ver_chequera_disponible'),
    path('ver-cuenta-bancaria/', views.VerCuentaBancaria,
         name='ver_cuenta_bancaria'),
    path('ver-cuenta-banciaria-todas/', views.VerCuentaBancariaTodas,
         name='ver_cuenta_bancaria_todas'),
    path('ver-chequera-alerta/', views.VerChequeraAlerta,
         name='ver_chequera_alerta'),
    path('ver-chequera-agotado/', views.VerChequeraAgotado,
         name='ver_chequera_agotado'),
    path('ver-chequera-disponible/', views.VerChequeraDisponible,
         name='ver_chequera_disponible'),
    path('ver-cuenta-bancaria/', views.VerCuentaBancaria,
         name='ver_cuenta_bancaria'),
    path('ver-cuenta-bancaria-todas/', views.VerCuentaBancariaTodas,
         name='ver_cuenta_bancaria_todas'),
    path('ver-cuenta-bancaria-activa/', views.VerCuentaBancariaActiva,
         name='ver_cuenta_bancaria_activa'),
    path('ver-cuenta-banciaria-no-activa/', views.VerCuentaBancariaNoActiva,
         name='ver_cuenta_bancaria_no_activa'),
]
