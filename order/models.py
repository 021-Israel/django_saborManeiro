from django.db import models
from djmoney.models.fields import MoneyField
from django.core.validators import MinValueValidator
from django.db.models import Case, When, Value, IntegerField
from django.conf import settings

class ProdutoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            ordem_categoria=Case(
                When(categoria_produto='LAN', then=Value(1)),
                When(categoria_produto='PTP', then=Value(2)),
                When(categoria_produto='BEB', then=Value(3)),
                When(categoria_produto='COM', then=Value(4)),
                When(categoria_produto='SOB', then=Value(5)),
                default=Value(99),
                output_field=IntegerField(),
            )
        ).order_by('ordem_categoria', 'nome_produto')

class Produto(models.Model):
    CATEGORIAS = [
        ('LAN', 'Lanches'),
        ('PTP', 'Pratos Principais'),
        ('BEB', 'Bebidas'),
        ('SOB', 'Sobremesas'),
        ('COM', 'Combos'),
    ]

    id_produto = models.AutoField(primary_key=True, verbose_name="ID")
    categoria_produto = models.CharField(
        max_length=3,
        choices=CATEGORIAS,
        default='LAN',
        verbose_name="Categoria"
    )
    nome_produto = models.CharField(max_length=30, verbose_name="Nome")
    foto_produto_url = models.URLField(
        max_length=500, 
        blank=True, 
        null=True,
        verbose_name="URL da Foto"
    ) 
    desc_produto = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Descrição"
    )
    preco_produto = MoneyField(
        max_digits=14, 
        decimal_places=2, 
        default_currency='BRL',
        validators=[MinValueValidator(0)],
        verbose_name="Preço"
    )
    disponivel = models.BooleanField(default=True, verbose_name="Disponível")

    objects = ProdutoManager()

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['nome_produto']

    def __str__(self):
        return f"{self.nome_produto} ({self.get_categoria_produto_display()}) - R$ {self.preco_produto}"




class Carrinho(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='carrinho'
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Carrinho"
        verbose_name_plural = "Carrinhos"

    def str(self):
        return f"Carrinho de {self.usuario.username}"

    @property
    def total(self):
        return sum(item.subtotal for item in self.itens.all())

    @property
    def total_itens(self):
        return sum(item.quantidade for item in self.itens.all())

class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(
        Carrinho, 
        related_name='itens',
        on_delete=models.CASCADE
    )
    produto = models.ForeignKey(
        Produto, 
        on_delete=models.CASCADE,
        related_name='itens_carrinho'
    )
    quantidade = models.PositiveIntegerField(default=1)
    adicionado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Item do Carrinho"
        verbose_name_plural = "Itens do Carrinho"
        unique_together = ['carrinho', 'produto']

    def str(self):
        return f"{self.quantidade}x {self.produto.nome_produto}"

    @property
    def subtotal(self):
        return self.produto.preco_produto * self.quantidade

class Pedido(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('PREPARO', 'Em preparo'),
        ('ENTREGA', 'Saiu para entrega'),
        ('ENTREGUE', 'Entregue'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pedidos'
    )
    data_pedido = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDENTE'
    )
    
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-data_pedido']
    
    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='itens'
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT
    )
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"
    
    @property
    def subtotal(self):
        return self.preco_unitario * self.quantidade
    
    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome_produto} (Pedido #{self.pedido.id})"