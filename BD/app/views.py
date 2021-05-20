from django.shortcuts import render
from .forms import FormUsuario

# Create your views here.
## Modificado

def Index(request):

    variable = 'Hola mundo'

    return render(request, 'inicio.html', {
        'titulo': 'Plantilla Principal',
        'variable': variable
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