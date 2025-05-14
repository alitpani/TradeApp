from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Trade
from decimal import Decimal
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class TradeAPITests(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test trades
        self.trade1 = Trade.objects.create(
            type='buy',
            user_id=23,
            symbol='ABX',
            shares=30,
            price=Decimal('134.00')
        )
        
        self.trade2 = Trade.objects.create(
            type='sell',
            user_id=23,
            symbol='XYZ',
            shares=50,
            price=Decimal('200.00')
        )
        
        # Setup API client
        self.client = APIClient()
        
        # Get JWT token
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_get_all_trades(self):
        """Test retrieving all trades"""
        url = reverse('trade-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_trade_by_id(self):
        """Test retrieving a specific trade"""
        url = reverse('trade-detail', kwargs={'pk': self.trade1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['symbol'], 'ABX')

    def test_create_trade(self):
        """Test creating a new trade"""
        url = reverse('trade-list')
        data = {
            'type': 'buy',
            'user_id': 24,
            'symbol': 'AAPL',
            'shares': 25,
            'price': '150.00'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Trade.objects.count(), 3)

    def test_create_trade_invalid_shares(self):
        """Test creating a trade with invalid shares"""
        url = reverse('trade-list')
        data = {
            'type': 'buy',
            'user_id': 24,
            'symbol': 'AAPL',
            'shares': 101,  # Invalid shares
            'price': '150.00'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_trade_invalid_type(self):
        """Test creating a trade with invalid type"""
        url = reverse('trade-list')
        data = {
            'type': 'invalid',
            'user_id': 24,
            'symbol': 'AAPL',
            'shares': 25,
            'price': '150.00'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_trades_by_type(self):
        """Test filtering trades by type"""
        url = reverse('trade-list')
        response = self.client.get(f'{url}?type=buy')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['type'], 'buy')

    def test_filter_trades_by_user_id(self):
        """Test filtering trades by user_id"""
        url = reverse('trade-list')
        response = self.client.get(f'{url}?user_id=23')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_trade_not_allowed(self):
        """Test that updating a trade is not allowed"""
        url = reverse('trade-detail', kwargs={'pk': self.trade1.id})
        data = {'shares': 40}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_trade_not_allowed(self):
        """Test that deleting a trade is not allowed"""
        url = reverse('trade-detail', kwargs={'pk': self.trade1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_unauthorized_access(self):
        """Test unauthorized access to trades"""
        self.client.credentials()  # Remove authentication
        url = reverse('trade-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class JWTAuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_obtain_token(self):
        """Test obtaining JWT token"""
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_refresh_token(self):
        """Test refreshing JWT token"""
        # First get the tokens
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        refresh_token = response.data['refresh']

        # Now try to refresh the access token
        url = reverse('token_refresh')
        data = {'refresh': refresh_token}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
