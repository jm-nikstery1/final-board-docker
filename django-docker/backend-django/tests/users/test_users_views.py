import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

MyUser = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    def make_user(**kwargs):
        return MyUser.objects.create_user(**kwargs)
    return make_user

@pytest.mark.django_db
def test_user_register(api_client):
    url = reverse('user-sign-up')
    data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword123',
        'password2': 'testpassword123'
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert MyUser.objects.filter(email='testuser@example.com').exists()

@pytest.mark.django_db
def test_user_login(api_client, create_user):
    user = create_user(
        username='testuser',
        email='testuser@example.com',
        password='testpassword123'
    )
    url = reverse('user-login')
    data = {
        'email': 'testuser@example.com',
        'password': 'testpassword123'
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data

@pytest.mark.django_db
def test_username_update(api_client, create_user):
    user = create_user(
        username='testuser',
        email='testuser@example.com',
        password='testpassword123'
    )
    api_client.force_authenticate(user=user)
    url = reverse('username-update', kwargs={'myuser_id': user.id})
    data = {
        'username': 'newusername',
        'password': 'testpassword123'
    }
    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.username == 'newusername'

@pytest.mark.django_db
def test_password_update(api_client, create_user):
    user = create_user(
        username='testuser',
        email='testuser@example.com',
        password='testpassword123'
    )
    api_client.force_authenticate(user=user)
    url = reverse('password-update', kwargs={'myuser_id': user.id})
    data = {
        'old_password': 'testpassword123',
        'password': 'newpassword123',
        'password2': 'newpassword123'
    }
    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.check_password('newpassword123')


@pytest.mark.django_db
def test_get_user_list(api_client, create_user):
    user1 = create_user(
        username='user1',
        email='user1@example.com',
        password='password123'
    )
    user2 = create_user(
        username='user2',
        email='user2@example.com',
        password='password123'
    )
    api_client.force_authenticate(user=user1)
    url = reverse('user-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['user_list']) == 2
    assert response.data['user_list'][0]['username'] == 'user1'
    assert response.data['user_list'][1]['username'] == 'user2'


@pytest.mark.django_db
def test_user_registration_and_login(api_client):

    register_url = reverse('user-sign-up')
    register_data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword123',
        'password2': 'testpassword123'
    }
    register_response = api_client.post(register_url, register_data)
    assert register_response.status_code == status.HTTP_204_NO_CONTENT
    assert MyUser.objects.filter(email='testuser@example.com').exists()

    login_url = reverse('user-login')
    login_data = {
        'email': 'testuser@example.com',
        'password': 'testpassword123'
    }
    login_response = api_client.post(login_url, login_data)
    assert login_response.status_code == status.HTTP_200_OK
    assert 'access' in login_response.data
    assert 'refresh' in login_response.data

@pytest.mark.django_db
def test_user_update_and_logout(api_client, create_user):

    user = create_user(
        username='testuser',
        email='testuser@example.com',
        password='testpassword123'
    )
    api_client.force_authenticate(user=user)

    username_update_url = reverse('username-update', kwargs={'myuser_id': user.id})
    username_update_data = {
        'username': 'newusername',
        'password': 'testpassword123'
    }
    username_update_response = api_client.put(username_update_url, username_update_data)
    assert username_update_response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.username == 'newusername'

    password_update_url = reverse('password-update', kwargs={'myuser_id': user.id})
    password_update_data = {
        'old_password': 'testpassword123',
        'password': 'newpassword123',
        'password2': 'newpassword123'
    }
    password_update_response = api_client.put(password_update_url, password_update_data)
    assert password_update_response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.check_password('newpassword123')

    login_url = reverse('user-login')
    login_data = {
        'email': 'testuser@example.com',
        'password': 'newpassword123'
    }
    login_response = api_client.post(login_url, login_data)
    assert login_response.status_code == status.HTTP_200_OK
    assert 'refresh' in login_response.data

    logout_url = reverse('logout_view')
    logout_data = {
        'refresh': login_response.data['refresh']
    }
    logout_response = api_client.post(logout_url, logout_data)
    assert logout_response.status_code == status.HTTP_200_OK
