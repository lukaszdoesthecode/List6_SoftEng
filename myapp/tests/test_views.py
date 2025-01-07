from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status
from django.urls import reverse
from myapp.models import Product


class ProductApiTest(APITestCase):
    def setUp(self):
        self.regular_user = User.objects.create_user(username='testuser', password='testpassword')
        self.admin = User.objects.create_superuser(username='testadmin', password='testpassword')

        self.product = Product.objects.create(name='Temporary product', price=1.99, available=True)

        self.product_list_url = reverse('product-list')
        self.product_detail_url = reverse('product-detail', kwargs={'pk': self.product.id})

        self.client = APIClient()

    # GET (all products)
    def test_get_all_products_as_regular_user(self):
        token = str(AccessToken.for_user(self.regular_user))
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Temporary product')

    def test_get_all_products_as_admin(self):
        token = str(AccessToken.for_user(self.admin))
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Temporary product')

    # GET (single product)
    def test_get_single_product_as_regular_user(self):
        token = str(AccessToken.for_user(self.regular_user))
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Temporary product')

    def test_get_single_product_as_admin(self):
        token = str(AccessToken.for_user(self.admin))
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Temporary product')

    # POST
    def test_create_product_as_regular_user(self):
        token = str(AccessToken.for_user(self.regular_user))
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        data = {"name": "Temporary Product 2", "price": 4.99, "available": True}
        response = self.client.post(self.product_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Regular users can't create products

    def test_create_product_as_admin(self):
        token = str(AccessToken.for_user(self.admin))
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        data = {"name": "Temporary Product 2", "price": 4.99, "available": True}
        response = self.client.post(self.product_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Temporary Product 2')

    # PATCH
    def test_modify_product_as_regular_user(self):
        token = str(AccessToken.for_user(self.regular_user))
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        data = {"name": "Modified Product"}
        response = self.client.patch(self.product_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Regular users can't modify products

    def test_modify_product_as_admin(self):
        token = str(AccessToken.for_user(self.admin))
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        data = {"name": "Modified Product"}
        response = self.client.patch(self.product_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Modified Product')

    # DELETE
    def test_delete_product_as_regular_user(self):
        token = str(AccessToken.for_user(self.regular_user))
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Regular users can't delete products

    def test_delete_product_as_admin(self):
        token = str(AccessToken.for_user(self.admin))
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    # Negative Test Cases
    # -----------------------

    def test_get_all_products_without_authentication(self):
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_single_product_with_invalid_id(self):
        token = str(AccessToken.for_user(self.admin))
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        invalid_url = reverse('product-detail', kwargs={'pk': 999})
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_product_with_missing_fields_as_admin(self):
        token = str(AccessToken.for_user(self.admin))
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        data = {"name": ""}
        response = self.client.post(self.product_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_with_invalid_price_type_as_admin(self):
        token = str(AccessToken.for_user(self.admin))
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        data = {"name": "Invalid Product", "price": "invalid_price", "available": True}
        response = self.client.post(self.product_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_modify_product_with_invalid_data_as_admin(self):
        token = str(AccessToken.for_user(self.admin))
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        data = {"price": "invalid_price"}
        response = self.client.patch(self.product_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_product_with_invalid_id_as_admin(self):
        token = str(AccessToken.for_user(self.admin))
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        invalid_url = reverse('product-detail', kwargs={'pk': 999})
        response = self.client.delete(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_product_without_authentication(self):
        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_modify_product_without_authentication(self):
        data = {"name": "Modified Product"}
        response = self.client.patch(self.product_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_product_without_authentication(self):
        data = {"name": "Unauthenticated Product", "price": 4.99, "available": True}
        response = self.client.post(self.product_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)