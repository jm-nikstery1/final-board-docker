import pytest
from django.contrib.auth import get_user_model

MyUser = get_user_model()

@pytest.mark.django_db
def test_create_user():
    user = MyUser.objects.create_user(
        email='testuser@example.com',
        username='testuser',
        password='testpassword123'
    )
    assert user.email == 'testuser@example.com'
    assert user.username == 'testuser'
    assert user.check_password('testpassword123')
    assert not user.is_admin

@pytest.mark.django_db
def test_create_superuser():
    user = MyUser.objects.create_superuser(
        email='admin@example.com',
        username='admin',
        password='adminpassword123'
    )
    assert user.email == 'admin@example.com'
    assert user.username == 'admin'
    assert user.check_password('adminpassword123')
    assert user.is_admin

@pytest.mark.django_db
def test_user_str():
    user = MyUser.objects.create_user(
        email='testuser@example.com',
        username='testuser',
        password='testpassword123'
    )
    assert str(user) == 'testuser@example.com'
