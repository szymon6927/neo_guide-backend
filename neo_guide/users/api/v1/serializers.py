from django.db import transaction
from django.utils.translation import gettext as _
from rest_framework import serializers

from neo_guide.users.models import User


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'confirm_password', 'first_name', 'last_name', 'city', 'parish', 'community')
        extra_kwargs = {'password': {'write_only': True}}

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
            raise serializers.ValidationError(_('Podaj hasło i potwierdź je.'))

        if password != confirm_password:
            raise serializers.ValidationError(_('Hasła się nie zgadzają'))

        return data
