from django.db import models

# Create your models here.
class Balancas(models.Model):
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    

    def __str__(self):
        return self.marca
    
class Clientes(models.Model):
    nome = models.CharField(max_length=100)
    contato = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
    
class Orcamentos(models.Model):
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    balanca = models.ForeignKey(Balancas, on_delete=models.CASCADE)
    num_serie_balanca = models.CharField(max_length=100, null=True, blank=True)
    data_chegada = models.DateField()
    data_entrega = models.DateField(null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    problema_pelo_cliente = models.CharField(max_length=300, null=True, blank=True)
    orcamento = models.CharField(max_length=300, null=True, blank=True)
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.orcamento
