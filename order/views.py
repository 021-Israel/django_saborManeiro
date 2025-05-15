from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from order.serializers import ProdutoSerializer
from order.models import Produto, Carrinho, ItemCarrinho, Pedido, ItemPedido
from django.http import JsonResponse
from django.contrib import messages

@login_required
def order(request):
    carrinho, created = Carrinho.objects.get_or_create(usuario=request.user)
    contexto = {
        'titulo': 'Pedido',
        'produtos': troca_categoria(request),
        'carrinho': carrinho
    }
    return render(request, 'order/index.html', contexto)

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

def troca_categoria(request):
    categoria = request.GET.get('categoria') or request.POST.get('categoria')
    if categoria:
        return Produto.objects.filter(categoria_produto=categoria)
    return Produto.objects.all()

@login_required
def ver_carrinho(request):
    carrinho = get_object_or_404(Carrinho, usuario=request.user)
    return render(request, 'order/ver_carrinho.html', {'carrinho': carrinho})

@login_required
def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id_produto=produto_id)
    
    if not produto.disponivel:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Produto indisponível'})
        messages.error(request, "Este produto não está disponível no momento.")
        return redirect('order:order')

    carrinho, created = Carrinho.objects.get_or_create(usuario=request.user)
    item, item_created = ItemCarrinho.objects.get_or_create(
        carrinho=carrinho,
        produto=produto,
        defaults={'quantidade': 1}
    )

    if not item_created:
        item.quantidade += 1
        item.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'total_itens': carrinho.total_itens,
            'message': f"{produto.nome_produto} adicionado ao carrinho!"
        })
    
    messages.success(request, f"{produto.nome_produto} adicionado ao carrinho!")
    return redirect(request.META.get('HTTP_REFERER', 'order:order'))

@login_required
def remover_do_carrinho(request, item_id):
    item = get_object_or_404(ItemCarrinho, id=item_id, carrinho__usuario=request.user)
    produto_nome = item.produto.nome_produto
    item.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        carrinho = Carrinho.objects.get(usuario=request.user)
        return JsonResponse({
            'success': True,
            'total_itens': carrinho.total_itens,
            'total': float(carrinho.total),
            'message': f"{produto_nome} removido do carrinho!"
        })
    
    messages.success(request, f"{produto_nome} removido do carrinho!")
    return redirect('order:ver_carrinho')

@login_required
def atualizar_carrinho(request, item_id):
    item = get_object_or_404(ItemCarrinho, id=item_id, carrinho__usuario=request.user)
    nova_quantidade = int(request.POST.get('quantidade', 1))

    if nova_quantidade > 0:
        item.quantidade = nova_quantidade
        item.save()
        messages.success(request, "Quantidade atualizada!")
    else:
        item.delete()
        messages.success(request, "Item removido do carrinho!")

    return redirect('order:ver_carrinho')

@login_required
def finalizar_pedido(request):
    try:
        carrinho = Carrinho.objects.get(usuario=request.user)
        
        if not carrinho.itens.exists():
            messages.warning(request, "Seu carrinho está vazio!")
            return redirect('order:ver_carrinho')

        total = sum(item.subtotal for item in carrinho.itens.all())
        pedido = Pedido.objects.create(
            usuario=request.user,
            total=total,
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