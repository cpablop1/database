from django.shortcuts import render

# Create your views here.
## Modificado

def Index(request):

    return render(request, 'layout.html', {
        'titulo': 'Plantilla Principal'
    })