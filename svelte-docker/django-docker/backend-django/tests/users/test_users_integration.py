import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

MyUser = get_user_model()

'''
백엔드 부분에서는 
Integration 테스트가 E2E 테스트랑 비슷하다 
'''

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_user_registration_and_login(api_client):
    # 사용자 등록
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

    # 사용자 로그인
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
    # 사용자 생성 및 로그인
    user = create_user(
        username='testuser',
        email='testuser@example.com',
        password='testpassword123'
    )
    api_client.force_authenticate(user=user)

    # 사용자 이름 수정
    username_update_url = reverse('username-update', kwargs={'myuser_id': user.id})
    username_update_data = {
        'username': 'newusername',
        'password': 'testpassword123'
    }
    username_update_response = api_client.put(username_update_url, username_update_data)
    assert username_update_response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.username == 'newusername'

    # 사용자 비밀번호 수정
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

    # 로그아웃
    logout_url = reverse('logout_view')
    logout_data = {
        'refresh': str(user.refresh_token)
    }
    logout_response = api_client.post(logout_url, logout_data)
    assert logout_response.status_code == status.HTTP_205_RESET_CONTENT

@pytest.mark.django_db
def test_user_list(api_client, create_user):
    # 사용자 생성
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

    # 사용자 목록 조회
    user_list_url = reverse('user-list')
    response = api_client.get(user_list_url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['user_list']) == 2
    assert response.data['user_list'][0]['username'] == 'user1'
    assert response.data['user_list'][1]['username'] == 'user2'
