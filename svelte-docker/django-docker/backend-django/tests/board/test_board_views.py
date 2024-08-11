import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from board.models import Post, Comment

MyUser = get_user_model()

'''
JWT 사용을 위해서는 client.force_authenticate 이걸 어떻게 사용해야할까
# DB에 있는 실제 유저로 해야하나 - jwt 의 활용 생각해야함

urls은 실제 url 주소로 하는데 
urls 에 보면 post 생성은 post.id 가 중요하지 않지만
get, update, delete 이건 post.id 가 필수로 해야함 - 이럴때는 실제 데이터로 해야하는지?
아니면 pytest.mark.django_db 로 이용해서 db에서 알아서 데이터 넣고 롤백?
유닛 테스트 , 통합 테스트, 엔드포인트 테스트 생각


'''

@pytest.mark.django_db
def test_create_post():
    client = APIClient()

    user = MyUser.objects.create_user(username='testuser', email='testuser123@test.com', password='testpass')
    client.force_authenticate(user=user)

    data = {
        'subject': 'Test Subject',
        'content': 'Test Content',
    }

    url = reverse('create_post')
    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_204_NO_CONTENT
    post = Post.objects.get(subject='Test Subject')
    assert post.content == 'Test Content'
    assert post.user == user

@pytest.mark.django_db
def test_create_post_invalid_data():
    client = APIClient()

    user = MyUser.objects.create_user(username='testuser', email='testuser123@test.com', password='testpass')
    client.force_authenticate(user=user)  # DB에 있는 실제 유저로 해야하나 - jwt 의 활용 생각해야함

    data = {
        'content': 'Test Content',
    }

    url = reverse('create_post')  # 실제 url 로 해야함
    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'subject' in response.data

@pytest.mark.django_db
def test_create_post_unauthenticated():
    client = APIClient()

    data = {
        'subject': 'Test Subject',
        'content': 'Test Content',
    }

    url = reverse('create_post')
    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_get_post():
    client = APIClient()

    user = MyUser.objects.create_user(username='testuser', email='testuser123@test.com', password='testpass')
    post = Post.objects.create(user=user, subject='Test Subject', content='Test Content')

    url = reverse('get_post', args=[post.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['subject'] == post.subject
    assert response.data['content'] == post.content

@pytest.mark.django_db
def test_update_post():
    client = APIClient()

    user = MyUser.objects.create_user(username='testuser', email='testuser123@test.com', password='testpass')
    client.force_authenticate(user=user)

    post = Post.objects.create(user=user, subject='Test Subject', content='Test Content')

    data = {
        'subject': 'Updated Subject',
        'content': 'Updated Content',
    }

    url = reverse('update_post', args=[post.id])
    response = client.put(url, data, format='json')

    assert response.status_code == status.HTTP_200_OK
    post.refresh_from_db()
    assert post.subject == 'Updated Subject'
    assert post.content == 'Updated Content'

@pytest.mark.django_db
def test_delete_post():
    client = APIClient()

    user = MyUser.objects.create_user(username='testuser', email='testuser123@test.com', password='testpass')
    client.force_authenticate(user=user)

    post = Post.objects.create(user=user, subject='Test Subject', content='Test Content')

    url = reverse('delete_post', args=[post.id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    with pytest.raises(Post.DoesNotExist):
        Post.objects.get(id=post.id)
