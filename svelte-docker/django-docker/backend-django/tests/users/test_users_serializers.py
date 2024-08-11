import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from users.serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserNameUpdateSerializer,
    UserPasswordUpdateSerializer,
    UserInfoSerializer,
)

MyUser = get_user_model()

@pytest.mark.django_db
def test_user_register_serializer():
    data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword123',
        'password2': 'testpassword123'
    }
    serializer = UserRegisterSerializer(data=data)
    assert serializer.is_valid()
    user = serializer.save()
    assert user.username == 'testuser'
    assert user.email == 'testuser@example.com'
    assert user.check_password('testpassword123')

@pytest.mark.django_db
def test_user_register_serializer_password_mismatch():
    data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword123',
        'password2': 'wrongpassword'
    }
    serializer = UserRegisterSerializer(data=data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)

@pytest.mark.django_db
def test_user_login_serializer():
    user = MyUser.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='testpassword123'
    )
    data = {
        'email': 'testuser@example.com',
        'password': 'testpassword123'
    }
    serializer = UserLoginSerializer(data=data)
    assert serializer.is_valid()

@pytest.mark.django_db
def test_user_name_update_serializer():
    user = MyUser.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='testpassword123'
    )
    data = {
        'username': 'newusername',
        'password': 'testpassword123'
    }
    serializer = UserNameUpdateSerializer(instance=user, data=data)
    assert serializer.is_valid()
    updated_user = serializer.save()
    assert updated_user.username == 'newusername'

@pytest.mark.django_db
def test_user_password_update_serializer():
    user = MyUser.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='oldpassword123'
    )
    data = {
        'old_password': 'oldpassword123',
        'password': 'newpassword123',
        'password2': 'newpassword123'
    }
    serializer = UserPasswordUpdateSerializer(instance=user, data=data)
    assert serializer.is_valid()
    updated_user = serializer.save()
    assert updated_user.check_password('newpassword123')

@pytest.mark.django_db
def test_user_info_serializer():
    user = MyUser.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='testpassword123'
    )
    serializer = UserInfoSerializer(user)
    assert serializer.data['username'] == 'testuser'
    assert serializer.data['email'] == 'testuser@example.com'
