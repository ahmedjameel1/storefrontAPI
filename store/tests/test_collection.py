from rest_framework import status
from store.models import Collection, Product
import pytest
from model_bakery import baker

@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections/', collection)
    return do_create_collection

@pytest.mark.django_db
class TestCreateCollection:
    
    def test_anonymous_returns_401(self, create_collection):
        response = create_collection({'title': 'a'})
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_not_admin_returns_403(self, authenticate, create_collection):
        response = create_collection({'title': 'a'})
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_data_invalid_returns_400(self, authenticate_admin, create_collection):
        response = create_collection({'title': ''})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None
    
    def test_data_valid_returns_201(self, authenticate_admin, create_collection):
        response = create_collection({'title': 'a'})
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db   
class TestRetrieveCollection:
    def test_if_collection_exists_returns_200(self, api_client):
        collection = baker.make(Collection)
        
        response = api_client.get(f'/store/collections/{collection.id}/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': collection.id,
            'title': collection.title,
            'products_count': 0
        }
        
@pytest.mark.django_db
class TestUpdateCollection:
    def test_anonymous_update_returns_401(self, api_client):
        collection = baker.make(Collection)
        
        response = api_client.patch(f'/store/collections/{collection.id}/', data={'title': 'u'})
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_not_admin_update_returns_403(self, api_client, authenticate):
        collection = baker.make(Collection)
        
        response = api_client.patch(f'/store/collections/{collection.id}/', data={'title': 'u'})
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    def test_admin_not_valid_returns_400(self, api_client, authenticate_admin):
        collection = baker.make(Collection)
        
        response = api_client.patch(f'/store/collections/{collection.id}/', data={'title': ''})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None
        
    def test_bad_pk_returns_404(self, api_client, authenticate_admin):
        response = api_client.patch('/store/collections/999/', data={'title': 'u'})
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_admin_valid_returns_200(self, api_client, authenticate_admin):
        collection = baker.make(Collection)
        
        response = api_client.patch(f'/store/collections/{collection.id}/', data={'title': 'u'})
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'u'
        
@pytest.mark.django_db
class TestDeleteCollections:
    def test_anonymous_delete_returns_401(self, api_client):
        collection = baker.make(Collection)
        
        response = api_client.delete(f'/store/collections/{collection.id}/')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_admin_delete_returns_204(self, api_client, authenticate_admin):
        collection = baker.make(Collection)
        
        response = api_client.delete(f'/store/collections/{collection.id}/')
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
    def test_admin_delete_with_products_in_collection_returns_405(self, api_client, authenticate_admin):
        collection = baker.make(Collection)
        products = [baker.make(Product), baker.make(Product)]
        for product in products:
            collection.products.add(product)
        
        response = api_client.delete(f'/store/collections/{collection.id}/')
        
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    