import pytest
from board.models import Post
from django.contrib.auth import get_user_model

MyUser = get_user_model()

@pytest.mark.django_db
def test_post_model():
    user = MyUser.objects.create_user(username='testuser', email='testuser123@test.com', password='testpass')
    post = Post.objects.create(user=user, subject='Test Subject', content='Test Content')

    assert post.user == user
    assert post.subject == 'Test Subject'
    assert post.content == 'Test Content'
