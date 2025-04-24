from django.shortcuts import render

# Create your views here.
def historia(request):
    contexto = {
        'titulo' : 'História'
    }
    return render(
        request,
        'historia/index.html',
        contexto
    )