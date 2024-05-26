from rest_framework import status
from core.models import User
from store.models import Collection, Customer, Order, OrderItem, Product, ProductImage
import pytest
from model_bakery import baker


@pytest.fixture
def create_product(api_client):
    def do_create_product(product):
        return api_client.post('/store/products/', product)
    return do_create_product
       
@pytest.mark.django_db
class TestCreateProduct:
    def test_anonymous_returns_401(self, create_product):
        response = create_product({'title': 'a'})
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_not_admin_returns_403(self, authenticate, create_product):
        response = create_product({'title': 'a'})
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    def test_invalid_returns_400(self, authenticate_admin, create_product):
        response = create_product({'title': ''})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None
        
    def test_valid_returns_201(self, authenticate_admin, create_product):
        product = {
            "title": "a",
            "slug": "a",
            "inventory": 0,
            "unit_price": 1,
            "collection": baker.make(Collection).id,
        }
        images = [{'image': baker.make(ProductImage)}, {'image': baker.make(ProductImage)}]
        product['images'] = images
        
        
        response = create_product(product)
        
        assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
class TestRetrieveProducts:
    def test_anonymous_retreive_returns_200(self, api_client):
        product = baker.make(Product)
        
        response = api_client.get(f'/store/products/{product.id}/')
        
        assert response.status_code == status.HTTP_200_OK
        
    def test_anonymous_retrieve_reviews_returns_200(self, api_client):
        product = baker.make(Product)
        
        response = api_client.get(f'/store/products/{product.id}/reviews/')
        
        assert response.status_code == status.HTTP_200_OK
        
@pytest.mark.django_db
class TestUpdateProducts:
    def test_anonymous_returns_401(self, api_client):
        product = baker.make(Product)
        
        response = api_client.patch(f'/store/products/{product.id}/', data={'title': 'u'})
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_not_admin_returns_403(self, api_client, authenticate):
        product = baker.make(Product)
        
        response = api_client.patch(f'/store/products/{product.id}/', data={'title': 'u'})

        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    def test_admin_invalid_returns_400(self, api_client, authenticate_admin):
        product = baker.make(Product)
        
        response = api_client.patch(f'/store/products/{product.id}/', data={'title': ''})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None
        
    def test_admin_valid_returns_200(self, api_client, authenticate_admin):
        product = baker.make(Product)
        
        response = api_client.patch(f'/store/products/{product.id}/', data={'title': 'u'})
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'u'

@pytest.mark.django_db        
class TestDeleteProducts:
    def test_anonymous_delete_returns_401(self, api_client):
        product = baker.make(Product)
        
        response = api_client.delete(f'/store/products/{product.id}/')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_not_admin_returns_403(self, api_client, authenticate):
        product = baker.make(Product)
        
        response = api_client.delete(f'/store/products/{product.id}/')
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    def test_admin_associated_with_order_items_returns_405(self, api_client, authenticate_admin):
        product = baker.make(Product,
                                orderitems=[baker.make(OrderItem,
                                    order=baker.make(Order,
                                        customer=baker.make(Customer,
                                                    user_id=2
                                                    )
                                        )
                                    )]
                            )
                
        response = api_client.delete(f'/store/products/{product.id}/')
        
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        
    def test_admin_not_associated_with_order_items_returns_204(self, api_client, authenticate_admin):
        product = baker.make(Product)
        
        response = api_client.delete(f'/store/products/{product.id}/')
        
        assert response.status_code == status.HTTP_204_NO_CONTENT