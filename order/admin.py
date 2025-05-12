from django.contrib import admin


# Register your models here.
from .models import Produto


admin.site.register(Produto)

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome_produto', 'categoria_produto', 'preco_produto')
    list_filter = ('categoria_produto',)
    search_fields = ('nome_produto',)