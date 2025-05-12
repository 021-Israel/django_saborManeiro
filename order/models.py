from django.db import models
from djmoney.models.fields import MoneyField

# Create your models here.
class Produto(models.Model):
    CATEGORIAS = [
        ('LAN', 'Lanches'),
        ('PTP', 'Pratos Principais'),
        ('BEB', 'Bebidas'),
        ('SOB', 'Sobremesas'),
        ('COM', 'Combos'),
    ]
    id_produto   = models.AutoField(primary_key=True)
    categoria_produto = models.CharField(
        max_length=3,
        choices=CATEGORIAS,
        default='LAN'
    )
    nome_produto = models.CharField(max_length=30)
    foto_produto_url = models.URLField(max_length = 500, blank=True, null=True) 
    desc_produto = models.TextField(blank=True, null=True)
    preco_produto = MoneyField(max_digits=14, decimal_places=2, default_currency='BRL')

    def __str__(self):
        return self.nome_produto + " Categoria: " +self.categoria_produto
    
