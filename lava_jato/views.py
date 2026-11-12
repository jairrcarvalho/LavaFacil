from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.utils import timezone
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
def dashboard(request):
    lavagens = Lavagem.objects.all().order_by('-data_hora')
    total_lavagens = lavagens.count()
    valor_semana = sum(
        lavagem.valor for lavagem in lavagens.filter(
            data_hora__week = timezone.now().isocalendar().week,
            data_hora__year = timezone.now().year
        )
    )
    valor_mes = sum(
        lavagem.valor for lavagem in lavagens.filter(
            data_hora__month= timezone.now().month,
            data_hora__year= timezone.now().year
        )
    )
    
#Resumos por categoria de veiculo
    resumo_moto = resumo_por_veiculo(lavagens, 'moto')
    resumo_carro = resumo_por_veiculo(lavagens, 'carro')
    resumo_caminhao = resumo_por_veiculo(lavagens, 'caminhão')
    resumo_trator = resumo_por_veiculo(lavagens, 'trator')
    
  
    context = {
        'lavagens': lavagens,
        'total_lavagens': total_lavagens,
        'valor_semana': valor_semana,
        'valor_mes': valor_mes,
        'resumo_moto': resumo_moto,
        'resumo_carro': resumo_carro,
        'resumo_caminhao': resumo_caminhao,
        'resumo_trator': resumo_trator,
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



