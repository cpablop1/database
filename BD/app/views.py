from django.shortcuts import render

# Create your views here.
## Modificado

def Index(request):

    return render(request, 'index.html', {
        'titulo': 'Plantilla Principal'
    })