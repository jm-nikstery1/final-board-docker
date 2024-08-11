import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from board.models import Post  # Post 모델 임포트

MyUser = get_user_model()

'''
JWT 사용을 위해서는 client.force_authenticate 이걸 어떻게 사용해야할까
# DB에 있는 실제 유저로 해야하나 - jwt 의 활용 생각해야함

urls은 실제 url 주소로 하는데 
urls 에 보면 post 생성은 post.id 가 중요하지 않지만
get, update, delete 이건 post.id 가 필수로 해야함 - 이럴때는 실제 데이터로 해야하는지?
아니면 pytest.mark.django_db 로 이용해서 db에서 알아서 데이터 넣고 롤백?
유닛 테스트 , 통합 테스트, 엔드포인트 테스트 생각

백엔드 부분에서는 
Integration 테스트가 E2E 테스트랑 비슷하다 

그리고 test 폴더안에 폴더로 다르게 구분한다해도 
test_models.py 이름이 동일한 이름은 사용못함
'''

@pytest.mark.django_db
def test_create_post():
    client = APIClient()

    # 유저 생성 및 인증
    user = MyUser.objects.create_user(email='testuser123@test.com', username='testuser123', password='testpass')
    client.force_authenticate(user=user)  # DB에 있는 실제 유저로 해야하나 - jwt 의 활용 생각해야함

    # 게시글 생성 데이터
    data = {
        'subject': 'Test Subject',
        'content': 'Test Content',
    }

    # API 요청
    url = reverse('create_post')  # 실제 url 로 해야함
    response = client.post(url, data, format='json')

    # 응답 코드 확인
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # 게시글이 생성되었는지 확인
    post = Post.objects.get(subject='Test Subject')
    assert post.content == 'Test Content'
    assert post.user == user

@pytest.mark.django_db
def test_create_post_invalid_data():
    client = APIClient()

    # 유저 생성 및 인증
    user = MyUser.objects.create_user(username='testuser', email='testuser123@test.com', password='testpass')
    client.force_authenticate(user=user)

    # 잘못된 게시글 생성 데이터 (subject가 없음)
    data = {
        'content': 'Test Content',
    }

    # API 요청
    url = reverse('create_post')  # create_post 뷰에 대한 URL 이름이 'create_post'라고 가정
    response = client.post(url, data, format='json')

    # 응답 코드 확인
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'subject' in response.data

@pytest.mark.django_db
def test_create_post_unauthenticated():
    client = APIClient()

    # 게시글 생성 데이터
    data = {
        'subject': 'Test Subject',
        'content': 'Test Content',
    }

    # 인증되지 않은 상태에서 API 요청
    url = reverse('create_post')  # create_post 뷰에 대한 URL 이름이 'create_post'라고 가정
    response = client.post(url, data, format='json')

    # 응답 코드 확인
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
