from hashlib import sha512
import hmac

from django.forms import ValidationError
from django.shortcuts import get_object_or_404

from rest_framework import serializers

from user.models import Image, Leader, Logins, User

from project.services.login_manager import login_leader, login_user
from project.settings import SECRET_KEY



class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    name = serializers.CharField(required=True)
    age = serializers.IntegerField()
    gender = serializers.IntegerField(required=False)
    race = serializers.IntegerField(required=False)
    phone_number = serializers.CharField(required=False)

    def validate(self, data):
        if User.objects.filter(email__iexact=data["email"]).exists():
            raise ValidationError("this email is already registered")
        if not 18 <= data["age"] <= 100:
            raise ValidationError("invalid age")
        data["password"] = hmac.new(SECRET_KEY.encode(), data["password"].encode(),sha512).hexdigest()
        return data
    
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = get_object_or_404(User , email__iexact=data["email"])
        if user.password != hmac.new(SECRET_KEY.encode(), data["password"].encode(),sha512).hexdigest():
            raise ValidationError("invalid passowrd")
        data["user"] = user
        return data
    
    def create(self, validated_data):
        user = validated_data["user"]
        login_data = login_user(user)
        Logins.objects.create(user=user,token=login_data.pop("token_id"))
        self._data = login_data
        return True


class CreateImageSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True, allow_null=False)
    type = serializers.IntegerField(required=True)
    id = serializers.IntegerField(read_only=True)

    def validate(self, data):
        if data["type"] not in dict(Image.TYPES):
            raise ValidationError("invalid type")
        return data

    def create(self, validated_data):
        user = self.context["request"].customer
        image = Image.objects.create(user=user, image=validated_data["image"], type=validated_data["type"])
        return image


class LeaderLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        leader = get_object_or_404(Leader , email__iexact=data["email"])
        if leader.password != hmac.new(SECRET_KEY.encode(), data["password"].encode(),sha512).hexdigest():
            raise ValidationError("invalid passowrd")
        data["leader"] = leader
        return data
    
    def create(self, validated_data):
        leader = validated_data["leader"]
        login_data = login_leader(leader)
        self._data = login_data
        return True
    

class UserListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["id","name","age","email","phone_number","gender","race","created_at"]
        read_only_fields = ["id","name","age","email","phone_number","gender","race","created_at"]


class ImageListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Image
        fields = "__all__"
        read_only_fields = ["id","image", "attemp", "type","created_at"]
