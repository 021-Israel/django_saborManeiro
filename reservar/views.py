from django.shortcuts import render, redirect
from .models import Pessoa

# Create your views here.
def reservar(request):
    contexto = {
        'titulo' : 'Reservar'
    }
    return render(
        request,
        'reservar/index.html',
        contexto
    )

def gravar(request):
    if request.method == 'POST':
        nova_pessoa = Pessoa()
        nova_pessoa.nome = request.POST.get('nome')
        nova_pessoa.sobrenome = request.POST.get('sobrenome')
        nova_pessoa.email = request.POST.get('email')
        nova_pessoa.data = request.POST.get('data')
        nova_pessoa.comentarios = request.POST.get('comentarios')
        nova_pessoa.convidados = request.POST.get('convidados')
        nova_pessoa.save()

        return redirect('/reservar?sucesso=1')