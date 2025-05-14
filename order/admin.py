from django.contrib import admin
from .models import Produto, Carrinho, ItemCarrinho


admin.site.register(Carrinho)
admin.site.register(ItemCarrinho)

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome_produto', 'categoria_produto', 'preco_produto']
    list_filter = ['categoria_produto']
    search_fields = ['nome_produto']