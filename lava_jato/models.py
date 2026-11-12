from django.db import models

# Create your models here.

class Lavagem(models.Model):
    veiculo = models.CharField(max_length=100)
    data_hora = models.DateTimeField(auto_now_add= True)
    valor = models.DecimalField(max_digits =10, decimal_places = 2)
     
    class Meta:
        ordering = ['-data_hora']