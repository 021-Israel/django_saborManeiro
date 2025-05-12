from django.shortcuts import render, redirect
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    contexto = {
        'titulo' : 'Inicial'
    }
    return render(
        request,
        'home/index.html',
        contexto
    )

def criarUser(request):
   
    if request.method=='POST':
        nome = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        User.objects.create_user(username = nome, email = email, password = password)
        return redirect('login')
    
    return render(
        request,
        'home/index.html')