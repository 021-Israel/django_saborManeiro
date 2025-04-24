from django.shortcuts import render

# Create your views here.
def galeria(request):
    contexto = {
        'titulo' : 'Galeria'
    }
    return render(
        request,
        'galeria/index.html',
        contexto
    )