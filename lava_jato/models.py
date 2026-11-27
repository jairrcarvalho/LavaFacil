from django.db import models
from django.conf import settings

# Create your models here.

class Lavagem(models.Model):
    usuario = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='lavagens',
    
    )
    veiculo = models.CharField(max_length=100)
    data_hora = models.DateTimeField(auto_now_add= True)
    valor = models.DecimalField(max_digits =10, decimal_places = 2)
     
    class Meta:
        ordering = ['-data_hora']