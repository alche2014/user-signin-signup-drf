from rest_framework import serializers
from django.db.models import Q
from django.contrib.auth import get_user_model
User = get_user_model()


class UserLoginSerializers(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
        ]

    def validate(self, data):
        email = data['email']
        password = data['password']
        user_queryset = User.objects.filter(Q(email__iexact=email) | Q(username__iexact=email)).distinct()

        if user_queryset.exists() and user_queryset.count() == 1:
            user_set = user_queryset.first()
            if user_set.check_password(password):
                user = user_set
                print(user)

            else:
                raise serializers.ValidationError("Incorrect Password!")

        else:
            raise serializers.ValidationError("Not Valid User!")
        return data


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
          username=validated_data['username'],
          password=validated_data['password'],
          email=validated_data['email'],
        )
        user.save()
        return user
