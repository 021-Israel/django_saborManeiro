from django.db import models

# Create your models here.

class Pessoa(models.Model):
    id_Pessoa = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    sobrenome = models.CharField(max_length=255)
    email = models.EmailField()

    data = models.DateField(null=True, blank=True)
    comentarios = models.TextField(null=True, blank=True)
    convidados = models.IntegerField(null=True, blank=True)
