from rest_framework import serializers
from users.models import User
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(
        max_length=127,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="email already registered.",
            )
        ],
    )
    username = serializers.CharField(
        max_length=50,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="username already taken.",
            )
        ],
    )
    birthdate = serializers.DateField(allow_null=True, default=None)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    is_employee = serializers.BooleanField(default=False, allow_null=True)
    is_superuser = serializers.BooleanField(read_only=True)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data: dict) -> User:
        if validated_data["is_employee"]:
            return User.objects.create_superuser(**validated_data)

        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        for key, value in validated_data.items():
            if key == "password":
                new_password = value
            setattr(instance, key, value)

        instance.save()

        user_password = User.objects.get(username=instance.username)
        user_password.set_password(new_password)
        user_password.save()

        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, write_only=True)
    password = serializers.CharField(write_only=True)
