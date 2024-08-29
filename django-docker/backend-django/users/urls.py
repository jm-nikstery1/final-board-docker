from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenRefreshView 
from .views import UserLoginAPIView, UserRegisterAPIView, Logout_User_jwt
from .views import UserNameUpdateAPIView, UserPasswordUpdateAPIView
from .views import GoogleLoginView, GoogleOAuthCallbackView, get_user_list 

from dj_rest_auth.registration.views import VerifyEmailView  # 이메일 인증



urlpatterns = [
    path("sign-up/", UserRegisterAPIView.as_view(), name="user-sign-up"),  # 소셜 로그인 기능이 없는 회원가입 
    path("login/", UserLoginAPIView.as_view(), name="user-login"),   # 소셜 로그인 기능이 없는 로그인
    path("token/refresh/", TokenRefreshView.as_view(), name="user-token-refresh"),  # restframework simple jwt 의 access, refresh 토큰을 재발급

    # 사용자 이름 수정
    path("username-update/<int:myuser_id>/", UserNameUpdateAPIView.as_view(), name="username-update"),

    # 사용자 비밀 번호 수정
    path("password-update/<int:myuser_id>/", UserPasswordUpdateAPIView.as_view(), name="password-update"),

    # jwt 로그아웃 - jwt 토큰을 블랙리스트에 넣어 로그아웃
    path("logout/", Logout_User_jwt.as_view(), name='logout_view'),

    # 유저 확인용
    path("user-list/", get_user_list, name='user-list'),

    path('dj-rest-auth/', include('dj_rest_auth.urls')),   # dj-rest-auth 의 기본 urls 모음 - 공식문서
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),   # dj-rest-auth 의 등록 urls 모음 - 공식문서

    path('accounts/', include('allauth.urls')),   # allauth 기능 


    path("google/login/callback/", GoogleOAuthCallbackView.as_view(), name="api_accounts_google_oauth_callback"),
    path("google/login/", GoogleLoginView.as_view(), name="api_accounts_google_oauth"),

    # 이메일 인증 - 회원가입시 - 등록한 이메일 검증임
    #re_path(r'^account-confirm-email/$', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    # 유저가 클릭한 이메일(=링크) 확인
    #re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(), name='account_confirm_email'),

]
