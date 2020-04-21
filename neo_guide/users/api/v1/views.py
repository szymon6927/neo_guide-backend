from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from neo_guide.core.api.v1.permissions import IsAdminUser
from neo_guide.core.api.v1.permissions import IsLoggedInUserOrAdmin
from neo_guide.users.api.v1.serializers import CreateUserSerializer
from neo_guide.users.api.v1.serializers import UserSerializer
from neo_guide.users.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    serializers = {'default': UserSerializer, 'create': CreateUserSerializer}

    def get_permissions(self):
        permission_mapper = {
            'create': [AllowAny],
            'retrieve': [IsLoggedInUserOrAdmin],
            'update': [IsLoggedInUserOrAdmin],
            'partial_update': [IsLoggedInUserOrAdmin],
            'list': [IsAdminUser],
            'destroy': [IsAdminUser],
            'me': [IsLoggedInUserOrAdmin],
        }

        permission_classes = permission_mapper.get(self.action)

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    @action(methods=['GET'], detail=False)
    def me(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user)

        return Response(serializer.data)
