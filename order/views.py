from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from order.serializers import ProdutoSerializer
from order.models import Produto


@login_required
def order(request):
    contexto = {
        'titulo' : 'Pedido',
        'produtos' : troca_categoria(request),
    }
    return render(
        request,
        'order/index.html',
        contexto
    )


# Create your views here.
class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer


def troca_categoria(request):
    categoria = request.GET.get('categoria') or request.POST.get('categoria')
    if categoria:
        return Produto.objects.filter(categoria_produto=categoria)
    return Produto.objects.all()