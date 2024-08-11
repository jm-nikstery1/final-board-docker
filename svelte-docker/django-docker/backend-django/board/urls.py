from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import get_post, get_id_post, like_post, create_post, delete_post, update_post,\
    create_comment, update_comment, delete_comment, like_comment, get_comment, get_id_comment

router = DefaultRouter()


urlpatterns = router.urls + [
    path('post/list/', get_post, name='post_list'),
    path('post/create/', create_post, name='create_post'),
    path('post/get/<int:post_id>/', get_id_post, name='get_post'),
    path('post/update/<int:post_id>/', update_post, name='update_post'),
    path('post/delete/<int:post_id>/', delete_post, name='delete_post'),
    path('post/likes/<int:post_id>/', like_post, name='like_post'),

    path('comment/list/', get_comment, name='get_comment'),
    path('comment/create/<int:post_id>/', create_comment, name='create_comment'),
    path('comment/get/<int:comment_id>/', get_id_comment, name='get_id_comment'),
    path('comment/update/<int:comment_id>/', update_comment, name='update_comment'),
    path('comment/delete/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('comment/likes/<int:comment_id>/', like_comment, name='like_comment'),
]
