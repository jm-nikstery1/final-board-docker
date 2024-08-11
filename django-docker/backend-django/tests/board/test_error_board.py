import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from board.models import Post, Comment

MyUser = get_user_model()


@pytest.mark.django_db
def test_error_create_post_invalid_data():
    client = APIClient()

    user = MyUser.objects.create_user(username='testuser', email='testuser123@test.com', password='testpassword123')
    client.force_authenticate(user=user)

    data = {
        'content': 'Test Content',
    }

    url = reverse('create_post')
    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'subject' in response.data

@pytest.mark.django_db
def test_error_create_post_authenticated():
    client = APIClient()

    data = {
        'subject': 'Test Subject',
        'content': 'Test Content',
    }

    url = reverse('create_post')
    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_error_create_comment_authenticated():
    client = APIClient()

    user = MyUser.objects.create_user(username='testuser', email='testuser123@test.com', password='testpassword123')
    post = Post.objects.create(user=user, subject='Test Subject', content='Test Content')

    data = {
        'text': 'Test Comment',
    }

    url = reverse('create_comment', args=[post.id])
    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED



@pytest.mark.django_db
def test_error_update_post_authenticated():
    client = APIClient()

    user_1 = MyUser.objects.create_user(username='testuser1', email='testuser1@test.com', password='testpassword123')
    client.force_authenticate(user=user_1)

    post = Post.objects.create(user=user_1, subject='test 제목', content='test 내용')

    user_2 = MyUser.objects.create_user(username='testuser2', email='testuser2@test.com', password='testpassword123')
    client.force_authenticate(user=user_2)

    data = {
        'subject': 'update 제목',
        'content': 'update 내용'
    }

    url = reverse('update_post', args=[post.id])
    response = client.put(url, data, format='json')

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data['detail'] == '게시글 수정 권한이 없습니다'



@pytest.mark.django_db
def test_error_update_comment_authenticated():
    client = APIClient()

    user_1 = MyUser.objects.create_user(username='testuser1', email='testuser1@test.com', password='testpassword123')
    client.force_authenticate(user=user_1)

    post = Post.objects.create(user=user_1, subject='test 제목', content='test 내용')
    comment = Comment.objects.create(user=user_1, post=post, text='test 답변')

    user_2 = MyUser.objects.create_user(username='testuser2', email='testuser2@test.com', password='testpassword123')
    client.force_authenticate(user=user_2)

    data = {
        'text': 'update 답변',
    }

    url = reverse('update_comment', args=[comment.id])
    response = client.put(url, data, format='json')

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data['detail'] == '댓글 수정 권한이 없습니다'



@pytest.mark.django_db
def test_error_delete_post_authenticated():
    client = APIClient()

    user_1 = MyUser.objects.create_user(username='testuser1', email='testuser1@test.com', password='testpassword123')
    client.force_authenticate(user=user_1)

    post = Post.objects.create(user=user_1, subject='test 제목', content='test 내용')

    client.force_authenticate(user=None)

    user_2 = MyUser.objects.create_user(username='testuser2', email='testuser2@test.com', password='testpassword123')
    client.force_authenticate(user=user_2)

    url = reverse('delete_post', args=[post.id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['detail'] == '게시글 삭제 권한이 없습니다'



@pytest.mark.django_db
def test_error_delete_post_authenticated():
    client = APIClient()

    user_1 = MyUser.objects.create_user(username='testuser1', email='testuser1@test.com', password='testpassword123')
    client.force_authenticate(user=user_1)

    post = Post.objects.create(user=user_1, subject='test 제목', content='test 내용')
    comment = Comment.objects.create(user=user_1, post=post, text='test 답변')

    client.force_authenticate(user=None)

    user_2 = MyUser.objects.create_user(username='testuser2', email='testuser2@test.com', password='testpassword123')
    client.force_authenticate(user=user_2)

    url = reverse('delete_comment', args=[comment.id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['detail'] == '댓글 삭제 권한이 없습니다'


@pytest.mark.django_db
def test_error_like_post_authenticated():
    client = APIClient()

    user = MyUser.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword123')
    client.force_authenticate(user=user)

    post = Post.objects.create(user=user, subject='test 제목', content='test 내용')

    client.force_authenticate(user=None)

    url = reverse('like_post', args=[post.id])
    response = client.post(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_error_like_comment_authenticated():
    client = APIClient()

    user = MyUser.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword123')
    client.force_authenticate(user=user)

    post = Post.objects.create(user=user, subject='test 제목', content='test 내용')
    comment = Comment.objects.create(user=user, post=post, text='test 답변')

    client.force_authenticate(user=None)

    url = reverse('like_comment', args=[comment.id])
    response = client.post(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

