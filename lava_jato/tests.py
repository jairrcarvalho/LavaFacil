
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal

from .models import Lavagem


class LavagemViewsTest(TestCase):

    def setUp(self):
        # Cria um usuário para os testes
        self.usuario = User.objects.create_user(
            username='teste',
            password='senha123'
        )

        # Faz login para acessar as páginas protegidas
        self.client.force_login(self.usuario)

        # Cria uma lavagem para usar nos testes
        self.lavagem = Lavagem.objects.create(
            veiculo='Carro',
            valor=Decimal('50.00')
        )

    def test_dashboard_abre(self):
        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'lava_jato/dashboard.html'
        )

    def test_historico_abre(self):
        response = self.client.get(reverse('historico'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'lava_jato/historico.html'
        )

    def test_registrar_lavagem(self):
        quantidade_inicial = Lavagem.objects.count()

        response = self.client.post(
            reverse('registrar_lavagem'),
            {
                'veiculo': 'Moto',
                'valor': '30.00',
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Lavagem.objects.count(),
            quantidade_inicial + 1
        )

        nova_lavagem = Lavagem.objects.latest('id')

        self.assertEqual(nova_lavagem.veiculo, 'Moto')
        self.assertEqual(nova_lavagem.valor, Decimal('30.00'))

    def test_editar_lavagem(self):
        data_original = self.lavagem.data_hora

        response = self.client.post(
            reverse(
                'editar_lavagem',
                args=[self.lavagem.id]
            ),
            {
                'veiculo': 'Moto',
                'valor': '40.00',
            }
        )

        self.assertEqual(response.status_code, 302)

        self.lavagem.refresh_from_db()

        self.assertEqual(self.lavagem.veiculo, 'Moto')
        self.assertEqual(self.lavagem.valor, Decimal('40.00'))

        # A data original não deve mudar
        self.assertEqual(
            self.lavagem.data_hora,
            data_original
        )

    def test_excluir_lavagem(self):
        response = self.client.post(
            reverse(
                'excluir_lavagem',
                args=[self.lavagem.id]
            )
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Lavagem.objects.filter(
                id=self.lavagem.id
            ).exists()
        )

    def test_usuario_nao_logado_nao_acessa_dashboard(self):
        self.client.logout()

        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 302)

    def test_login_com_credenciais_validas(self):
        self.client.logout()

        response = self.client.post(
            reverse('login'),
            {
                'username': 'teste',
                'password': 'senha123',
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            '_auth_user_id' in self.client.session
        )

    def test_login_com_senha_incorreta(self):
        self.client.logout()

        response = self.client.post(
            reverse('login'),
            {
                'username': 'teste',
                'password': 'senha_errada',
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'Nome de usuário ou senha inválidos.'
        )
