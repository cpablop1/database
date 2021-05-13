from django.shortcuts import render

# Create your views here.
## Modificado

def Index(request):

    variable = 'Hola mundo'

    return render(request, 'usuarios.html', {
        'titulo': 'Plantilla Principal',
        'variable': variable
    })

def Ver_usuario(respuesta):

    variable = 'Hola mundo!'

    return render(respuesta, 'ver_usuario.html', {
        'variable': variable
    })