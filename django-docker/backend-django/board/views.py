from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Post, Comment
from .serializers import PostSerializer, PostCreateSerializer, PostListSerializer, PostUpdateSerializer, \
    CommentSerializer, CommentCreateSerializer, CommentUpdateSerializer, CommentListSerializer

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from django.shortcuts import get_object_or_404
from django.db.models import Q

from django.contrib.auth import get_user_model

# CRUD
User = get_user_model()


@extend_schema(methods=['GET'],
               tags=['게시글'],
               summary="게시글 리스트 전체 조회",
               description="모든 게시글을 전체 조회합니다",
               parameters=[
                   OpenApiParameter(name='page', description='페이지 번호', required=False, type=int),
                   OpenApiParameter(name='size', description='한 페이지당 항목 수', required=False, type=int),
                   OpenApiParameter(name='keyword', description='검색 키워드', required=False, type=str),
                   ],
               responses={200: PostListSerializer(many=True)}
               )
@api_view(['GET'])
def get_post(request):
    queryset = Post.objects.all().order_by('-create_date')

    page = request.query_params.get('page', 0)
    size = request.query_params.get('size', 10)
    keyword = request.query_params.get('keyword', '')

    if keyword:
        queryset = queryset.filter(Q(subject__icontains=keyword))

    total = queryset.count()
    start = int(page) * int(size)
    end = start + int(size)
    queryset = queryset[start:end]

    serializer = PostSerializer(queryset, many=True)
    return Response({'total': total, 'posts': serializer.data})


@extend_schema(methods=['GET'],
               tags=['게시글'],
               summary="게시글 선택 조회",
               description="선택한 게시글을 조회합니다",
               parameters=[
                   OpenApiParameter(name='post_id_extend', description='post id', required=False, type=int),
                   ],
               responses={200: PostSerializer}
               )
@api_view(['GET'])
def get_id_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    serializer = PostSerializer(post)

    return Response(serializer.data)


@extend_schema(methods=['POST'],
               tags=['게시글'],
               summary="게시글 생성",
               description="새로운 게시글을 생성합니다.",
               request=PostCreateSerializer,
               responses={204: None}
               )
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    data = request.data

    serializer = PostCreateSerializer(data=data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
        methods=['PUT'],
        tags=['게시글'],
        summary='게시글 업데이트',
        description='게시글 업데이트 합니다',
        request=PostUpdateSerializer,
        )
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.user != post.user:
        return Response({'detail': '게시글 수정 권한이 없습니다'}, status=status.HTTP_403_FORBIDDEN)

    serializer = PostUpdateSerializer(post, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'detail': '게시글 수정 완료'}, status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
        methods=['DELETE'],
        tags=['게시글'],
        summary='게시글 삭제',
        description='게시글 삭제 합니다',
        )
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.user == post.user:
        post.delete()
        return Response({'detail': '게시글 삭제 완료'}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'detail': '게시글 삭제 권한이 없습니다'}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(methods=['POST'],
               tags=['게시글'],
               description="게시글 좋아요 추천")
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        message = '좋아요 취소 완료'
    else:
        post.likes.add(request.user)
        message = '좋아요 추가 완료'

    return Response({'detail': message}, status=status.HTTP_204_NO_CONTENT)


@extend_schema(methods=['POST'],
               tags=['댓글'],
               summary="댓글 생성",
               description="새로운 댓글을 생성합니다.",
               request=CommentCreateSerializer,
               responses={204: None}
               )
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    data = request.data
    data['post'] = post.pk
    serializer = CommentCreateSerializer(data=data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@extend_schema(methods=['GET'],
               tags=['댓글'],
               summary="댓글 전체 조회",
               description="모든 댓글을 전체 조회합니다",
               parameters=[
                   OpenApiParameter(name='page', description='페이지 번호', required=False, type=int),
                   OpenApiParameter(name='size', description='한 페이지당 항목 수', required=False, type=int),
                   ],
               responses={200: CommentListSerializer(many=True)}
               )
@api_view(['GET'])
def get_comment(request):
    queryset = Comment.objects.all()

    page = request.query_params.get('page', 0)
    size = request.query_params.get('size', 10)

    total = queryset.count()

    start = int(page) * int(size)
    end = start + int(size)
    queryset = queryset[start:end]

    serializer = CommentListSerializer(queryset, many=True)
    return Response({'total': total, 'comments': serializer.data})


@extend_schema(
        methods=['PUT'],
        tags=['댓글'],
        summary='댓글 업데이트',
        description='댓글 업데이트 합니다',
        request=CommentUpdateSerializer,
        )
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.user != comment.user:
        return Response({'detail': '댓글 수정 권한이 없습니다'}, status=status.HTTP_403_FORBIDDEN)

    serializer = CommentUpdateSerializer(comment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'detail': '댓글 수정 완료'}, status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
        methods=['GET'],
        tags=['댓글'],
        summary='댓글 조회',
        description='특정 게시글에 있는 댓글을 조회 합니다',
        )
@api_view(['GET'])
def get_id_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    serializer = CommentSerializer(comment)
    return Response(serializer.data)


@extend_schema(
        methods=['DELETE'],
        tags=['댓글'],
        summary='댓글 삭제',
        description='댓글 삭제 합니다',
        )
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.user == comment.user:
        comment.delete()
        return Response({'detail': '댓글 삭제 완료'}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'detail': '댓글 삭제 권한이 없습니다'}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(methods=['POST'],
               tags=['댓글'],
               description="댓글 좋아요 추천")
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
        message = '댓글 좋아요 취소 완료'
    else:
        comment.likes.add(request.user)
        message = '댓글 좋아요 추가 완료'

    return Response({'detail': message}, status=status.HTTP_204_NO_CONTENT)
