from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('registrar_lavagem/', views.registrar_lavagem, name='registrar_lavagem'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('historico/',views.historico, name = 'historico'),
    path('editar_lavagem/<int:lavagem_id>/', views.editar_lavagem, name='editar_lavagem'),
    path('excluir_lavagem/<int:lavagem_id>/', views.excluir_lavagem, name='excluir_lavagem'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'), 
      
]