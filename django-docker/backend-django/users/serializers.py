from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from rest_framework_simplejwt.serializers import (
    TokenBlacklistSerializer,
    TokenObtainPairSerializer,
)

MyUser = get_user_model()


# 회원가입
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError([{"비밀번호가 일치 하지 않습니다"}])
        validate_password(data['password'])
        return data

    def validate_username(self, username):
        if get_user_model().objects.filter(username=username).exists():
            raise serializers.ValidationError([{"이미 존재한 회원이름 입니다"}])
        return username

    def validate_email(self, value):
        if get_user_model().objects.filter(email=value).exists():
            raise serializers.ValidationError([{"이미 존재한 이메일 입니다"}])
        return value

    def create(self, validated_data):
        validated_data.pop('password2')
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class UserLoginSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        #token['password'] = user.password - password를 넣으면 암호화된 정보가 나타남
        token['email'] = user.email

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({
            'username': self.user.username,
            'password': self.user.password,
        })
        return data


# 회원 이름 수정
class UserNameUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField()

    class Meta:
        model = MyUser
        fields = ['username', 'password']

    def validate_password(self, password):
        if not self.instance.check_password(password):
            raise serializers.ValidationError([{"비밀번호가 일치 하지 않습니다"}])
        return password

    def validate_username(self, username):
        user = self.instance
        if user.username != username:
            if MyUser.objects.filter(username=username).exists():
                raise serializers.ValidationError([{"이미 존재한 회원이름 입니다"}])
        return username

    def update(self, instance, validated_data):
        instance.username = validated_data['username']
        instance.save()
        return instance


# 회원 비밀 번호 수정
class UserPasswordUpdateSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = MyUser
        fields = ['old_password', 'password', 'password2']

    def validate(self, data):
        user = self.instance

        if not user.check_password(data['old_password']):
            raise serializers.ValidationError({"현재 비밀번호가 일치 하지 않습니다"})

        if data['password'] != data['password2']:
            raise serializers.ValidationError({"비밀번호가 일치 하지 않습니다"})

        validate_password(data['password'], user)

        return data

    def update(self, instance, validated_data):
        validated_data.pop('old_password')
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

class LogoutSerializer(TokenBlacklistSerializer):

    pass


class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ['id', 'username', 'email']

