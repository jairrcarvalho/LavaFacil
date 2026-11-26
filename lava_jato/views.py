from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.utils import timezone
from datetime import datetime, timedelta, time
from decimal import Decimal
from django.db.models import Sum
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
        lavagem.valor = request.POST.get('valor')
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

@login_required
def dashboard(request):
    hoje = timezone.localdate()

    periodo = request.GET.get('periodo', 'mes')
    data_inicio = None
    data_fim = None
    erro_filtro = None

    # Definição dos períodos
    if periodo == 'semana':
        data_inicio = hoje - timedelta(days=hoje.weekday())
        data_fim = hoje
        nome_periodo = 'Semana atual'

    elif periodo == 'mes':
        data_inicio = hoje.replace(day=1)
        data_fim = hoje
        nome_periodo = 'Mês atual'

    elif periodo == '30dias':
        data_inicio = hoje - timedelta(days=29)
        data_fim = hoje
        nome_periodo = 'Últimos 30 dias'

    elif periodo == 'personalizado':
        try:
            data_inicio = datetime.strptime(
                request.GET.get('data_inicio', ''), '%Y-%m-%d'
            ).date()

            data_fim = datetime.strptime(
                request.GET.get('data_fim', ''), '%Y-%m-%d'
            ).date()

            if data_inicio > data_fim or data_fim > hoje:
                raise ValueError

            nome_periodo = 'Período personalizado'

        except ValueError:
            periodo = 'mes'
            data_inicio = hoje.replace(day=1)
            data_fim = hoje
            nome_periodo = 'Mês atual'
            erro_filtro = 'Informe um período válido.'

    else:
        periodo = 'mes'
        data_inicio = hoje.replace(day=1)
        data_fim = hoje
        nome_periodo = 'Mês atual'

    # Conversão para datetime com fuso horário
    inicio = timezone.make_aware(
        datetime.combine(data_inicio, time.min)
    )

    fim = timezone.make_aware(
        datetime.combine(data_fim + timedelta(days=1), time.min)
    )

    # Consulta das lavagens do período
    lavagens = Lavagem.objects.filter(
        data_hora__gte=inicio,
        data_hora__lt=fim
    ).order_by('-data_hora')

    # Indicadores
    total_lavagens = lavagens.count()

    valor_periodo = lavagens.aggregate(
        total=Sum('valor')
    )['total'] or Decimal('0.00')

    ticket_medio = (
        valor_periodo / total_lavagens
        if total_lavagens > 0
        else Decimal('0.00')
    )

    # Resumos por categoria
    resumo_moto = resumo_por_veiculo(lavagens, 'moto')
    resumo_carro = resumo_por_veiculo(lavagens, 'carro')
    resumo_caminhao = resumo_por_veiculo(lavagens, 'caminhão')
    resumo_trator = resumo_por_veiculo(lavagens, 'trator')

    context = {
        'lavagens': lavagens,
        'total_lavagens': total_lavagens,
        'valor_periodo': valor_periodo,
        'ticket_medio': ticket_medio,

        'resumo_moto': resumo_moto,
        'resumo_carro': resumo_carro,
        'resumo_caminhao': resumo_caminhao,
        'resumo_trator': resumo_trator,

        'periodo': periodo,
        'nome_periodo': nome_periodo,
        'data_inicio': data_inicio.strftime('%Y-%m-%d'),
        'data_fim': data_fim.strftime('%Y-%m-%d'),
        'erro_filtro': erro_filtro,
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



