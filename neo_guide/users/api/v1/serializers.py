from django.db import transaction
from django.utils.translation import gettext as _
from rest_framework import serializers

from neo_guide.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'city', 'parish', 'community')


class CreateUserSerializer(UserSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('password', 'confirm_password')
        extra_kwargs = {'password': {'write_only': True}, 'confirm_password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('confirm_password')

        with transaction.atomic():
            user = User(**validated_data)
            user.set_password(password)
            user.is_active = False
            user.save()

            return user

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if not password or not confirm_password:
            raise serializers.ValidationError(_('Enter the password and confirm it.'))

        if password != confirm_password:
            raise serializers.ValidationError(_('Passwords do not match!'))

        return data


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True, allow_blank=False)
    new_password = serializers.CharField(required=True, allow_blank=False)
    confirm_new_password = serializers.CharField(required=True, allow_blank=False)

    def validate(self, data):
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        confirm_new_password = data.get('confirm_new_password')

        if current_password == new_password or current_password == confirm_new_password:
            raise serializers.ValidationError(_('Passwords cannot be the same!'))

        if new_password != confirm_new_password:
            raise serializers.ValidationError(_('Passwords do not match!'))

        return data
