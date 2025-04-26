from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required



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


