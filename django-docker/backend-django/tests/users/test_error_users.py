import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.serializers import ValidationError
from users.serializers import UserRegisterSerializer

MyUser = get_user_model()

@pytest.mark.django_db
def test_error_create_user_long_username():
    data = {
        'email': 'test@test.com',
        'username': 'abcdefg가나다1234567890aa',
        'password': 'testpassword123',
        'password2': 'testpassword123',
    }
    serializer = UserRegisterSerializer(data=data)
    assert not serializer.is_valid() 
    assert 'username' in serializer.errors
    assert '이 필드의 글자 수가 20 이하인지 확인하십시오.' in str(serializer.errors['username'])


@pytest.mark.django_db
def test_error_create_user_duplicate_email():
    user_1_data = {
        'email': 'test@test.com',
        'username': 'test_user_1',
        'password': 'testpassword123',
        'password2': 'testpassword123'
    }
    user_1_serializer = UserRegisterSerializer(data=user_1_data)
    assert user_1_serializer.is_valid()
    user_1_serializer.save()

    user_2_data = {
        'email': 'test@test.com',
        'username': 'test_user_2',
        'password': 'testpassword123',
        'password2': 'testpassword123'
    }
    user_2_serializer = UserRegisterSerializer(data=user_2_data)
    with pytest.raises(ValidationError) as excinfo:
        user_2_serializer.is_valid(raise_exception=True)
    assert 'my user의 email은/는 이미 존재합니다.' in str(excinfo.value)


@pytest.mark.django_db
def test_error_create_user_duplicate_username():
    user_1_data = {
        'email': 'test1@test.com',
        'username': 'test_user',
        'password': 'testpassword123',
        'password2': 'testpassword123'
    }
    user_1_serializer = UserRegisterSerializer(data=user_1_data)
    assert user_1_serializer.is_valid()
    user_1_serializer.save()

    user_2_data = {
        'email': 'test2@test.com',
        'username': 'test_user',
        'password': 'testpassword123',
        'password2': 'testpassword123'
    }
    user_2_serializer = UserRegisterSerializer(data=user_2_data)
    with pytest.raises(ValidationError) as excinfo:
        user_2_serializer.is_valid(raise_exception=True)
    assert 'my user의 username은/는 이미 존재합니다.' in str(excinfo.value)


@pytest.mark.django_db
def test_error_create_user_short_password():
    data = {
        'email': 'test3@test.com',
        'username': 'test3_username',
        'password': '12345',
        'password2': '12345'
    }
    serializer = UserRegisterSerializer(data=data)
    with pytest.raises(ValidationError) as excinfo:
        serializer.is_valid(raise_exception=True)
    assert '비밀번호가 너무 짧습니다. 최소 8 문자를 포함해야 합니다.' in str(excinfo.value)


@pytest.mark.django_db
def test_error_create_user_simple_password():
    data = {
        'email': 'test3@test.com',
        'username': 'test3_username',
        'password': '12345678a',
        'password2': '12345678a'
    }
    serializer = UserRegisterSerializer(data=data)
    with pytest.raises(ValidationError) as excinfo:
        serializer.is_valid(raise_exception=True)
    assert '비밀번호가 너무 일상적인 단어입니다.' in str(excinfo.value)


@pytest.mark.django_db
def test_error_create_user_password_mismatch():
    data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword123',
        'password2': 'wrongpassword'
    }
    serializer = UserRegisterSerializer(data=data)
    with pytest.raises(ValidationError) as excinfo:
        serializer.is_valid(raise_exception=True)
    assert '비밀번호가 일치 하지 않습니다' in str(excinfo.value)


@pytest.mark.django_db
def test_error_update_same_username():
    client = APIClient()

    user_1 = MyUser.objects.create_user(
        username='testuser1',
        email='testuser1@example.com',
        password='testpassword123'
    )
    user_2 = MyUser.objects.create_user(
        username='testuser2',
        email='testuser2@example.com',
        password='testpassword123'
    )

    client.force_authenticate(user=user_1)

    url = reverse('username-update', kwargs={'myuser_id': user_1.id})
    data = {
        'username': 'testuser2',
    }
    response = client.put(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'username' in response.data
    assert '이미 존재한 회원이름 입니다' in response.data['username'][0]


@pytest.mark.django_db
def test_error_update_same_username():
    client = APIClient()

    user_1 = MyUser.objects.create_user(
        username='testuser1',
        email='testuser1@example.com',
        password='testpassword123'
    )
    user_2 = MyUser.objects.create_user(
        username='testuser2',
        email='testuser2@example.com',
        password='testpassword123'
    )

    client.force_authenticate(user=user_1)

    url = reverse('username-update', kwargs={'myuser_id': user_1.id})
    data = {
        'username': 'testuser2',
    }
    response = client.put(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'username' in response.data
    assert '이미 존재한 회원이름 입니다' in response.data['username'][0]
