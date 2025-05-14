from django.urls import path
from . import views
from .views import (ver_carrinho, adicionar_ao_carrinho,remover_do_carrinho, atualizar_carrinho)


app_name = 'order'

urlpatterns =[
    path('', views.order, name='order'),
    
    path('carrinho/', ver_carrinho, name='ver_carrinho'),
    
    path('carrinho/adicionar/<int:produto_id>/',
    adicionar_ao_carrinho, name='adicionar_ao_carrinho'),

    path('carrinho/remover/<int:item_id>/', 
    remover_do_carrinho, name='remover_do_carrinho'),

    path('carrinho/atualizar/<int:item_id>/', atualizar_carrinho, name='atualizar_carrinho'),

    path('finalizar-pedido/', views.finalizar_pedido, name='finalizar_pedido'),

]