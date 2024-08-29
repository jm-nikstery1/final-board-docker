import pytest
from board.models import Post, Comment
from board.serializers import (
    PostSerializer, PostCreateSerializer, PostUpdateSerializer, PostListSerializer,
    CommentSerializer, CommentCreateSerializer, CommentUpdateSerializer, CommentListSerializer
)
from django.contrib.auth import get_user_model

MyUser = get_user_model()

@pytest.mark.django_db
def test_post_serializer():
    user = MyUser.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword123')
    post = Post.objects.create(user=user, subject='test 제목', content='test 내용')

    serializer = PostSerializer(post)
    data = serializer.data

    assert data['user']['username'] == 'testuser'
    assert data['subject'] == 'test 제목'
    assert data['content'] == 'test 내용'
    assert data['likes'] == []
    assert 'comments' in data

@pytest.mark.django_db
def test_post_create_serializer():
    user = MyUser.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword123')
    data = {
        'subject': 'test 제목',
        'content': 'test 내용'
    }

    serializer = PostCreateSerializer(data=data)
    assert serializer.is_valid()

    post = serializer.save(user=user)
    assert post.subject == 'test 제목'
    assert post.content == 'test 내용'
    assert post.user == user

@pytest.mark.django_db
def test_post_update_serializer():
    user = MyUser.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword123')
    post = Post.objects.create(user=user, subject='test 제목', content='test 내용')

    data = {
        'subject': 'update 제목',
        'content': 'update 내용'
    }

    serializer = PostUpdateSerializer(post, data=data, partial=True)
    assert serializer.is_valid()

    updated_post = serializer.save()
    assert updated_post.subject == 'update 제목'
    assert updated_post.content == 'update 내용'

@pytest.mark.django_db
def test_comment_serializer():
    user = MyUser.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword123')
    post = Post.objects.create(user=user, subject='test 제목', content='test 내용')
    comment = Comment.objects.create(user=user, post=post, text='test 답변')

    serializer = CommentSerializer(comment)
    data = serializer.data

    assert data['user']['username'] == 'testuser'
    assert data['text'] == 'test 답변'
    assert data['likes'] == []
    assert data['post'] == post.id

@pytest.mark.django_db
def test_comment_create_serializer():
    user = MyUser.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword123')
    post = Post.objects.create(user=user, subject='test 제목', content='test 내용')

    data = {
        'post': post.id,
        'text': 'test 답변'
    }

    serializer = CommentCreateSerializer(data=data)
    assert serializer.is_valid()

    comment = serializer.save(user=user)
    assert comment.text == 'test 답변'
    assert comment.user == user
    assert comment.post == post

@pytest.mark.django_db
def test_comment_update_serializer():
    user = MyUser.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword123')
    post = Post.objects.create(user=user, subject='test 제목', content='test 내용')
    comment = Comment.objects.create(user=user, post=post, text='test 답변')

    data = {
        'text': 'update 답변'
    }

    serializer = CommentUpdateSerializer(comment, data=data, partial=True)
    assert serializer.is_valid()

    updated_comment = serializer.save()
    assert updated_comment.text == 'update 답변'


@pytest.mark.django_db
def test_post_list_serializer():
    user = MyUser.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword123')

    post1 = Post.objects.create(user=user, subject='test 제목 1', content='test 내용 1')
    post2 = Post.objects.create(user=user, subject='test 제목 2', content='test 내용 2')

    posts = Post.objects.all()

    serializer = PostListSerializer(posts, many=True)
    data = serializer.data

    assert len(data) == 2
    assert data[0]['subject'] == 'test 제목 1'
    assert data[1]['subject'] == 'test 제목 2'

    assert 'comments' in data[0] 
    assert 'comments' in data[1]
    assert data[0]['user']['email'] == 'testuser@test.com'
    assert data[1]['user']['username'] == 'testuser' 


@pytest.mark.django_db
def test_comment_list_serializer():
    user = MyUser.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword123')

    post1 = Post.objects.create(user=user, subject='test 제목 1', content='test 내용 1')
    post2 = Post.objects.create(user=user, subject='test 제목 2', content='test 내용 2')

    comment1 = Comment.objects.create(user=user, post=post1, text='test 답변 1')
    comment2 = Comment.objects.create(user=user, post=post2, text='test 답변 2')

    comments = Comment.objects.all()

    serializer = CommentListSerializer(comments, many=True)
    data = serializer.data

    assert len(data) == 2
    assert data[0]['text'] == 'test 답변 1'
    assert data[1]['text'] == 'test 답변 2'

    assert data[0]['user']['email'] == 'testuser@test.com' 
    assert data[1]['user']['username'] == 'testuser' 
