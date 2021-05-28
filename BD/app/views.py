from django.shortcuts import render
from .forms import FormUsuario

import data.rol as rol
import data.Contacto as Contacto

# Create your views here.
# Modificado


def Index(request):

    return render(request, 'layout.html')

def CrearRol(request):
    return render(request, 'crear_rol.html')


def Login(request):
    return render(request, 'login.html')


def CrearPermisos(request):
    if request.method == 'POST':
        dicccionario = {"nombre": "Cajero",                   
                "crud_users": 0,
                "imprimir_cheque": 1,
                "anular_cheque": 0,
                "modificar_cheque": 0,
                "reporte_cheque": 0,
                "auditar_user": 0,
                "admin_cuenta_banc": 0,
                "auditar_cuenta": 0,
                "mostrar_bitacora_user": 0,
                "mostrar_bitacora_group": 0,
                "mostrar_bitacora_jefe": 0,
                "jefe": 0}
            
        data = rol.Rol_permiso_sup()
        #resultado = data.create(dicccionario)
        resultado = data.read(2)
        print (resultado)
    return render(request, 'crear_permiso.html')

