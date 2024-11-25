from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Product, Order, OrderItem


class ProductTest(APITestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.product = Product.objects.create(
            name='Test product',
            description='A test description',
            price=19.99,
            stock=100
        )

    def test_list_products(self):
        url = reverse('product-list')  # Correct URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_product_authenticated(self):
        url = reverse('product-list')  # Correct URL name
        data = {'name': 'New Product', 'description': 'New Description', 'price': 20.00, 'stock': 10}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_product_unauthenticated(self):
        self.client.credentials()  # Clear authentication
        url = reverse('product-list')  # Correct URL name
        data = {'name': 'New Product', 'description': 'New Description', 'price': 20.00, 'stock': 10}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class OrderTest(APITestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.product = Product.objects.create(
            name='Test Product',
            description='Test Product Description',
            price=15.99,
            stock=50
        )
   
    def test_create_order_authenticated(self):
        url = reverse('order-list')
        data = {
            'items': [{'product': self.product.id, 'quantity': 2}]
        }
        response = self.client.post(url, data, format='json')
        print(response.data)  # Debug output to inspect the response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_orders_unauthenticated(self):
        self.client.credentials()  # Clear authentication
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticationTests(APITestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)

    def test_access_protected_endpoint_with_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_protected_endpoint_without_authentication(self):
        self.client.credentials()  # Clear authentication
        url = reverse('product-list')
        data = {'name': 'Unauthorized Product', 'description': 'No Auth', 'price': 10.00, 'stock': 1}
        response = self.client.post(url, data, format='json')  # POST requires authentication
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)