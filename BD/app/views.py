from django.shortcuts import render
from .forms import FormUsuario

# Create your views here.
## Modificado

def Index(request):
    return render(request, 'layout.html')

def CrearRol(request):
    return render(request, 'crear_rol.html')

def Login(request):
    return render(request, 'login.html')

def CrearPermisos(request):
    return render(request, 'crear_permiso.html')