from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView, status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.generics import get_object_or_404   # id 있는지 탐색

from .serializers import UserLoginSerializer, UserRegisterSerializer, UserInfoSerializer, LogoutSerializer, UserNameUpdateSerializer, UserPasswordUpdateSerializer

# 내가 추가한 것
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
)

from django.contrib.auth import get_user_model

# CRUD
MyUser = get_user_model()


@extend_schema(
        methods=['POST'],
        tags=['사용자'],
        summary="User 회원 가입 - 소셜 기능 없음",
        request=UserRegisterSerializer,
        description="User 회원 가입 - 소셜 기능 없음"
    )
@permission_classes([AllowAny])
class UserRegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            Token = TokenObtainPairSerializer.get_token(user)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@extend_schema(
        methods=['POST'],
        tags=['사용자'],
        summary='User 로그인 - 소셜 기능 없음',
        request=UserLoginSerializer,
        description='User 회원 로그인 - 소셜 기능 없음'
    )
class UserLoginAPIView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.user
        access_token = serializer.validated_data.get('access')
        refresh_token = serializer.validated_data.get('refresh')

        response_data = {
            'access': access_token,
            'refresh': refresh_token,
            'username': user.username,
            'myuser_id': user.id,
        }

        return Response(response_data)



@extend_schema(
        methods=['PUT'],
        tags=['사용자'],
        summary="사용자 회원 이름 수정 - 소셜 기능 없음",
        request=UserNameUpdateSerializer,
        description="사용자 회원 이름 수정 - 소셜 기능 없음"
    )
@permission_classes([IsAuthenticated])
class UserNameUpdateAPIView(APIView):

    def get_object(self, myuser_id):
        return get_object_or_404(MyUser, id=myuser_id)

    def put(self, request, myuser_id):
        user = self.get_object(myuser_id)
        serializer = UserNameUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()

            refresh = RefreshToken.for_user(user)

            new_tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            response_data = {
                'access': str(refresh),
                'refresh': str(refresh.access_token),
                'username': user.username,
                'myuser_id': user.id,
            }
            access_token = serializer.validated_data.get('access')
            refresh_token = serializer.validated_data.get('refresh')

            return Response({'tokens': new_tokens}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@extend_schema(
        methods=['PUT'],
        tags=['사용자'],
        summary="사용자 회원 비밀 번호 수정 - 소셜 기능 없음",
        request=UserPasswordUpdateSerializer,
        description="사용자 회원 비밀 번호 수정 - 소셜 기능 없음",

    )
@permission_classes([IsAuthenticated])
class UserPasswordUpdateAPIView(APIView):

    def get_object(self, myuser_id):
        return get_object_or_404(MyUser, id=myuser_id)

    def put(self, request, myuser_id):
        user = self.get_object(myuser_id)
        serializer = UserPasswordUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@extend_schema(
        methods=['POST'],
        tags=['사용자'],
        summary='User 호그아웃 -소셜 기능 있는 상황과 없는 상황 둘다 사용- refresh 토큰 넣기', request=LogoutSerializer,
        description='User 호그아웃 -소셜 기능 있는 상황과 없는 상황 둘다 사용- refresh 토큰을 blacklist 에 등록 - 프론트는 저장된 token 삭제')
class Logout_User_jwt(TokenBlacklistView):
    serializer = LogoutSerializer


@extend_schema(methods=['GET'],
               tags=['사용자'],
               summary="User 전체 조회 - 개발자 관리용 - 삭제할까? ",
               description="모든 User 전체 조회합니다 - 개발자용",
               parameters=[
                   OpenApiParameter(name='page', description='페이지 번호', required=False, type=int),
                   OpenApiParameter(name='size', description='한 페이지당 항목 수', required=False, type=int),
               ],
               responses={200: UserInfoSerializer(many=True)}
               )
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_list(request):
    queryset = MyUser.objects.all()

    page = request.query_params.get('page', 0)
    size = request.query_params.get('size', 10)

    start = int(page) * int(size)
    end = start + int(size)
    queryset = queryset[start:end]

    serializer = UserInfoSerializer(queryset, many=True)
    return Response({'user_list': serializer.data})




from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

import requests
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import redirect



@extend_schema(
    tags=['사용자 - OAuth2'],
    summary="사용자 - OAuth2 Callback - 성공시 리다이렉트와 쿠키 전송",
)
class GoogleOAuthCallbackView(APIView):

    def get(self, request: Request):
        # code 값을 URL의 query string에서 추출

        code = request.GET.get("code")
        if code:
            response = self.forward_code_to_google_login_view(code)
            if response.status_code == 200:
                # Google로부터 반환된 사용자 정보
                google_user_info = response.json()
                email = google_user_info['user']['email']
                user, created = MyUser.objects.get_or_create(email=email, defaults={'email': email})

                refresh = RefreshToken.for_user(user)

                tokens = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }

                response = redirect("http://localhost/#/oauth/callback/")   # nginx를 사용하기 때문에 변경
                response.set_cookie('access_token', tokens['access'], httponly=False, secure=False,
                                    samesite='Lax')
                response.set_cookie('refresh_token', tokens['refresh'], httponly=False, secure=False,
                                    samesite='Lax')
                response.set_cookie('username', str(user).split('@')[0], httponly=False, secure=False,
                                    samesite='Lax')

                return response

            return Response(
                {"error": "Failed to process with GoogleLoginView"},
                status=response.status_code,
            )

        return Response(
            {"error": "Code not provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    def forward_code_to_google_login_view(self, code: str):
        url = "http://localhost:8000/api/users/google/login/"
        payload = {"code": code}
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        return response


@extend_schema(
    tags=['사용자 - OAuth2'],
    summary="사용자 - OAuth2 loginview - allauth 가 필수",
)
class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'http://localhost:8000/api/users/google/login/callback/'
    client_class = OAuth2Client


"""
# 이메일 인증 - 새로운 소셜기능 없는 회원가입시 필요
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC


class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        confirmation.confirm(self.request)
        # A React Router Route will handle the failure scenario
        return HttpResponseRedirect('/')  # 인증성공

    def get_object(self, queryset=None):
        key = self.kwargs['key']
        email_confirmation = EmailConfirmationHMAC.from_key(key)
        if not email_confirmation:
            if queryset is None:
                queryset = self.get_queryset()
            try:
                email_confirmation = queryset.get(key=key.lower())
            except EmailConfirmation.DoesNotExist:
                # A React Router Route will handle the failure scenario
                return HttpResponseRedirect('/')  # 인증실패
        return email_confirmation

    def get_queryset(self):
        qs = EmailConfirmation.objects.all_valid()
        qs = qs.select_related("email_address__user")
        return qs
"""

