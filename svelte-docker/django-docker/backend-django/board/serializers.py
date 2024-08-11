from rest_framework import serializers
from users.serializers import UserInfoSerializer
from .models import Post, Comment

from django.contrib.auth import get_user_model

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "text", "create_date", "modify_date", "likes", "post"]


class CommentCreateSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "post", "text", "user"]


class CommentUpdateSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'user', 'modify_date']


class PostSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ["id", "user", "subject", "content", "create_date", "modify_date",
                  "likes", "comments"]


class PostCreateSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "subject", "content", "user"]


class PostUpdateSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'subject', 'content', 'user', 'modify_date']


class PostListSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'subject', 'create_date', 'modify_date', 'comments']


class CommentListSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)
    posts = PostSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'posts', 'create_date', 'modify_date']