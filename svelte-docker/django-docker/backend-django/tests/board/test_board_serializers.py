import pytest
from board.serializers import PostCreateSerializer
from board.models import Post
from django.contrib.auth import get_user_model

MyUser = get_user_model()


@pytest.mark.django_db
def test_post_create_serializer():
    user = MyUser.objects.create_user(username='testuser', email='testuser123@test.com', password='testpass')
    data = {
        'subject': 'Test Subject',
        'content': 'Test Content',
    }
    serializer = PostCreateSerializer(data=data)
    assert serializer.is_valid()
    post = serializer.save(user=user)

    assert post.subject == 'Test Subject'
    assert post.content == 'Test Content'
    assert post.user == user
