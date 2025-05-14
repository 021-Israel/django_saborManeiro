from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from order.serializers import ProdutoSerializer
from order.models import Produto, Carrinho, ItemCarrinho, Pedido, ItemPedido
from django.http import JsonResponse
from django.contrib import messages


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



def adicionar_ao_carrinho(request):
    produto_id = request.POST.get('id_produto')
    produto = get_object_or_404(Produto, id=produto_id)

    carrinho = request.session.get('carrinho', {})

    if produto_id in carrinho:
        carrinho[produto_id]['quantidade'] += 1
    else:
        carrinho[produto_id] = {
            'nome': produto.produto_nome,
            'preco': produto.produto_preco,
            'quantidade': 1
        }

    request.session['carrinho'] = carrinho
    return JsonResponse({'status': 'ok', 'total_itens': sum(item['quantidade'] for item in carrinho.values())})


def remover_do_carrinho(request):
    produto_id = request.POST.get('id_produto')
    carrinho = request.session.get('carrinho', {})

    if produto_id in carrinho:
        del carrinho[produto_id]
        request.session['carrinho'] = carrinho

    return JsonResponse({'status': 'ok'})


def obter_carrinho(request):
    carrinho = request.session.get('carrinho', {})
    total = sum(item['preco'] * item['quantidade'] for item in carrinho.values())

    return JsonResponse({
        'itens': carrinho,
        'total': total,
        'total_itens': sum(item['quantidade'] for item in carrinho.values())
    })

    
@login_required
def ver_carrinho(request):
    carrinho, created = Carrinho.objects.get_or_create(usuario=request.user)
    return render(request, 'carrinho/ver_carrinho.html', {'carrinho': carrinho})

@login_required
def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id_produto=produto_id)

    if not produto.disponivel:
        messages.error(request, "Este produto não está disponível no momento.")
        return redirect('cardapio:lista_produtos')

    carrinho, created = Carrinho.objects.get_or_create(usuario=request.user)


    item, item_created = ItemCarrinho.objects.get_or_create(
        carrinho=carrinho,
        produto=produto,
        defaults={'quantidade': 1}
    )

    if not item_created:
        item.quantidade += 1
        item.save()

    messages.success(request, f"{produto.nome_produto} adicionado ao carrinho!")
    return redirect(request.META.get('HTTP_REFERER', 'carrinho:ver_carrinho'))

@login_required
def remover_do_carrinho(request, item_id):
    item = get_object_or_404(
        ItemCarrinho, 
        id=item_id, 
        carrinhousuario=request.user
    )
    produto_nome = item.produto.nome_produto
    item.delete()
    messages.success(request, f"{produto_nome} removido do carrinho!")
    return redirect('carrinho:ver_carrinho')

@login_required
def atualizar_carrinho(request, item_id):
    item = get_object_or_404(
        ItemCarrinho, 
        id=item_id, 
        carrinhousuario=request.user
    )

    nova_quantidade = int(request.POST.get('quantidade', 1))

    if nova_quantidade > 0:
        item.quantidade = nova_quantidade
        item.save()
        messages.success(request, "Quantidade atualizada!")
    else:
        item.delete()
        messages.success(request, "Item removido do carrinho!")

    return redirect('carrinho:ver_carrinho')



@login_required
def finalizar_pedido(request):
    try:
        carrinho = Carrinho.objects.get(usuario=request.user)

        if not carrinho.itens.exists():
            messages.warning(request, "Seu carrinho está vazio!")
            return redirect('order:ver_carrinho')

        pedido = Pedido.objects.create(
            usuario=request.user,
            total=carrinho.total,
            status='PENDENTE'
        )

        for item in carrinho.itens.all():
            ItemPedido.objects.create(
                pedido=pedido,
                produto=item.produto,
                quantidade=item.quantidade,
                preco_unitario=item.produto.preco_produto
            )

        carrinho.itens.all().delete()

        messages.success(request, "Pedido realizado com sucesso!")
        return render(request, 'order/pedido_sucesso.html', {'pedido': pedido})

    except Carrinho.DoesNotExist:
        messages.error(request, "Carrinho não encontrado!")
        return redirect('order:ver_carrinho')

    