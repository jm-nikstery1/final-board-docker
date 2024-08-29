import pytest
from board.models import Post, Comment
from django.contrib.auth import get_user_model

MyUser = get_user_model()

@pytest.mark.django_db
def test_post_model():
    user = MyUser.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword123')
    post = Post.objects.create(user=user, subject='test 제목', content='test 내용')

    assert post.user == user
    assert post.subject == 'test 제목'
    assert post.content == 'test 내용'
    assert post.likes.count() == 0  

    post.likes.add(user) 
    assert post.likes.count() == 1
    assert post.likes.first() == user

    post.likes.remove(user) 
    assert post.likes.count() == 0

@pytest.mark.django_db
def test_comment_model():
    user = MyUser.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword123')
    post = Post.objects.create(user=user, subject='test 제목', content='test 내용')
    comment = Comment.objects.create(user=user, post=post, text='test 답변')

    assert comment.user == user
    assert comment.post == post
    assert comment.text == 'test 답변'
    assert comment.likes.count() == 0 

    comment.likes.add(user) 
    assert comment.likes.count() == 1
    assert comment.likes.first() == user

    comment.likes.remove(user) 
    assert comment.likes.count() == 0