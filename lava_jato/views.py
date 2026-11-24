from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.utils import timezone
from datetime import date, timedelta
from django.db.models import Sum, Count
from django.contrib import messages
from .services import resumo_por_veiculo
from .models import Lavagem
from django.core.paginator import Paginator
# Create your views here.



namespace = 'lava_jato'


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            request.session.set_expiry(1209600)
            
            return redirect('dashboard')
        else:
            error_message = 'Nome de usuário ou senha inválidos.'
            return render(
                request, 'lava_jato/login.html', 
                {'error_message': error_message})
            
    return render(request, 'lava_jato/login.html')


@login_required
def registrar_lavagem(request):
    
    if request.method == 'POST':
        veiculo = request.POST.get('veiculo')
        valor = request.POST.get('valor')
    
        Lavagem.objects.create(veiculo=veiculo, valor=valor)
        messages.success(request, 'Lavagem registrada com sucesso!')
        return redirect("dashboard")
        
        
    return render(request, 'lava_jato/registrar_lavagem.html')

@login_required
def editar_lavagem(request, lavagem_id):
    lavagem = get_object_or_404(Lavagem, id=lavagem_id)
    
    
    if request.method == 'POST':
        lavagem.veiculo = request.POST.get('veiculo')
        valor = request.POST.get('valor', '').strip()
        valor = valor.replace(",",".")
        lavagem.valor = valor
        lavagem.save()
        
        messages.info(request, 'Lavagem editada com sucesso!')
        return redirect('historico')
    
    return render(request, 'lava_jato/editar_lavagem.html', {'lavagem': lavagem})

@login_required
def excluir_lavagem(request, lavagem_id):
    
    lavagem = get_object_or_404(Lavagem, id=lavagem_id)
    
    if request.method == 'POST':
        
        lavagem.delete()
        messages.warning(request, 'Lavagem excluída com sucesso!')
        return redirect('historico')
    
    return redirect('historico')

@login_required
def dashboard(request):

    hoje = timezone.localdate()

    # Período selecionado
    periodo = request.GET.get('periodo', 'mes')

    data_inicio = None
    data_fim = hoje

    if periodo == 'hoje':
        data_inicio = hoje

    elif periodo == '7dias':
        data_inicio = hoje - timedelta(days=6)

    elif periodo == 'mes':
        data_inicio = hoje.replace(day=1)

    elif periodo == '30dias':
        data_inicio = hoje - timedelta(days= 9)

    elif periodo == 'personalizado':
        try:
            data_inicio = date.fromisoformat(
                request.GET.get('data_inicio', '')
            )
            data_fim = date.fromisoformat(
                request.GET.get('data_fim', '')
            )

            if data_inicio > data_fim:
                data_inicio = None
                data_fim = hoje

        except (ValueError, TypeError):
            data_inicio = hoje.replace(day=1)
            data_fim = hoje

    elif periodo == 'anterior':
        primeiro_dia_mes = hoje.replace(day=1)
        data_fim = primeiro_dia_mes - timedelta(days=1)
        data_inicio = data_fim.replace(day=1)

    # Consulta filtrada
    lavagens = Lavagem.objects.filter(
        data_hora__date__range=(data_inicio, data_fim)
    ).order_by('-data_hora')

    # Indicadores
    total_lavagens = lavagens.count()

    faturamento = lavagens.aggregate(
        total=Sum('valor')
    )['total'] or 0

    # Resumos por veículo
    resumo_moto = resumo_por_veiculo(lavagens, 'moto')
    resumo_carro = resumo_por_veiculo(lavagens, 'carro')
    resumo_caminhao = resumo_por_veiculo(lavagens, 'caminhão')
    resumo_trator = resumo_por_veiculo(lavagens, 'trator')

    context = {
        'lavagens': lavagens,
        'total_lavagens': total_lavagens,
        'faturamento': faturamento,
        'resumo_moto': resumo_moto,
        'resumo_carro': resumo_carro,
        'resumo_caminhao': resumo_caminhao,
        'resumo_trator': resumo_trator,
        'periodo': periodo,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }

    return render(request, 'lava_jato/dashboard.html', context)



@login_required
def historico(request):
    lavagens = Lavagem.objects.all().order_by('-data_hora')
    
    paginador = Paginator(lavagens, 15)
    pagina = request.GET.get('page')
    
    lavagens_paginadas = paginador.get_page(pagina)
        
    context = {
        'lavagens': lavagens_paginadas,
    }
    return render(request, 'lava_jato/historico.html', context)



