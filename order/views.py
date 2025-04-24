from django.shortcuts import render



# Create your views here.
def order(request):
    contexto = {
        'titulo' : 'Pedido'
    }
    return render(
        request,
        'order/index.html',
        contexto
    )


