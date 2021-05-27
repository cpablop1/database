from django.shortcuts import render
from .forms import FormUsuario

# Create your views here.
# Modificado


def Index(request):
    return render(request, 'layout.html')


<< << << < HEAD
   if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        celular = request.POST['celular']
        direccion = request.POST['direccion']
        correo = request.POST['correo']
        mensaje = request.POST['mensaje']

        print(nombre)
        print(apellido)
        print(celular)
        print(direccion)
        print(correo)
        print(mensaje)

    return render(request, 'layout.html', {

        'titulo': 'Plantilla Principal'
    })


def About(respuesta):

    return render(respuesta, 'about.html')


def Crear_usuario(respuesta):
    form = FormUsuario()

    if respuesta.method == 'POST':
        form = FormUsuario(respuesta.POST)
        if form.is_valid():
            form.save()

    return render(respuesta, 'usuario/crear_usuario.html', {
        'form': form
    })
== =====


def CrearRol(request):
    return render(request, 'crear_rol.html')


def Login(request):
    return render(request, 'login.html')


def CrearPermisos(request):
    return render(request, 'crear_permiso.html')
