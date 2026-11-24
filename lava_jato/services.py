from django.utils import timezone





def resumo_por_veiculo(lavagens, veiculo):
    
    lavagens_filtradas = lavagens.filter(
        veiculo__icontains = veiculo,
        data_hora__month = timezone.now().month,
        data_hora__year = timezone.now().year
    )
    
    resumo_qtd = lavagens_filtradas.count()
    resumo_valor = sum(lavagem.valor for lavagem in lavagens_filtradas)
    return {
        'quantidade': resumo_qtd,
        'valor': resumo_valor
    }
