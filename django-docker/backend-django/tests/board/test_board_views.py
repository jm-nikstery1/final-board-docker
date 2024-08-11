import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from board.models import Post, Comment

MyUser = get_user_model()


@pytest.mark.django_db
def test_create_post():
    client = APIClient()

    user = MyUser.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword123')
    client.force_authenticate(user=user)

    data = {
        'subject': 'test 제목',
        'content': 'test 내용'
    }

    url = reverse('create_post')
    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_204_NO_CONTENT
    post = Post.objects.get(subject='test 제목')
    assert post.content == 'test 내용'
    assert post.user == user


@pytest.mark.django_db
def test_get_post():
    client = APIClient()

    user = MyUser.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword123')
    post = Post.objects.create(user=user, subject='test 제목', content='test 내용')

    url = reverse('get_post', args=[post.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['subject'] == post.subject
    assert response.data['content'] == post.content

@pytest.mark.django_db
def test_update_post():
    client = APIClient()

    user = MyUser.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword123')
    client.force_authenticate(user=user)

    post = Post.objects.create(user=user, subject='test 제목', content='test 내용')

    data = {
        'subject': 'update 제목',
        'content': 'update 내용'
    }

    url = reverse('update_post', args=[post.id])
    response = client.put(url, data, format='json')

    assert response.status_code == status.HTTP_204_NO_CONTENT
    post.refresh_from_db()
    assert post.subject == 'update 제목'
    assert post.content == 'update 내용'

@pytest.mark.django_db
def test_delete_post():
    client = APIClient()

    user = MyUser.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword123')
    client.force_authenticate(user=user)

    post = Post.objects.create(user=user, subject='test 제목', content='test 내용')

    url = reverse('delete_post', args=[post.id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    with pytest.raises(Post.DoesNotExist):
        Post.objects.get(id=post.id)



@pytest.mark.django_db
def test_like_post():
    client = APIClient()

    user = MyUser.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword123')
    client.force_authenticate(user=user)

    post = Post.objects.create(user=user, subject='test 제목', content='test 내용')

    url = reverse('like_post', args=[post.id])
    response = client.post(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert post.likes.filter(id=user.id).exists()

    response = client.post(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not post.likes.filter(id=user.id).exists()



@pytest.mark.django_db
def test_create_comment():
    client = APIClient()

    user = MyUser.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword123')
    client.force_authenticate(user=user)

    post = Post.objects.create(user=user, subject='test 제목', content='test 내용')

    data = {
        'text': 'test 답변',
    }

    url = reverse('create_comment', args=[post.id])
    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Comment.objects.filter(post=post, user=user, text='test 답변').exists()



@pytest.mark.django_db
def test_update_comment():
    client = APIClient()

    user = MyUser.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword123')
    client.force_authenticate(user=user)

    post = Post.objects.create(user=user, subject='test 제목', content='test 내용')
    comment = Comment.objects.create(user=user, post=post, text='test 답변')

    data = {
        'text': 'update 답변',
    }

    url = reverse('update_comment', args=[comment.id])
    response = client.put(url, data, format='json')

    assert response.status_code == status.HTTP_204_NO_CONTENT
    comment.refresh_from_db()
    assert comment.text == 'update 답변'



@pytest.mark.django_db
def test_delete_comment():
    client = APIClient()

    user = MyUser.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword123')
    client.force_authenticate(user=user)

    post = Post.objects.create(user=user, subject='test 제목', content='test 내용')
    comment = Comment.objects.create(user=user, post=post, text='test 답변')

    url = reverse('delete_comment', args=[comment.id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    with pytest.raises(Comment.DoesNotExist):
        Comment.objects.get(id=comment.id)


@pytest.mark.django_db
def test_like_comment():
    client = APIClient()

    user = MyUser.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword123')
    client.force_authenticate(user=user)

    post = Post.objects.create(user=user, subject='test 제목', content='test 내용')
    comment = Comment.objects.create(user=user, post=post, text='test 답변')

    url = reverse('like_comment', args=[comment.id])
    response = client.post(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert comment.likes.filter(id=user.id).exists()

    response = client.post(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not comment.likes.filter(id=user.id).exists()