from django.contrib import admin
from .models import Pessoa

@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sobrenome', 'email', 'data', 'convidados')
    list_filter = ('data',)
    search_fields = ('nome', 'sobrenome', 'email')
