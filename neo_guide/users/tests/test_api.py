import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from neo_guide.users.models import User
from neo_guide.users.tests.factories import UserFactory


@pytest.mark.django_db
class TestUserListView:
    def test_get_users(self, api_client):
        api_client.force_authenticate(UserFactory.create_admin())

        UserFactory.create_batch(5)
        response = api_client.get(reverse('v1-users:user-list'))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == User.objects.count()

    def test_get_users_for_not_admin_user(self, api_client_with_token):
        UserFactory.create_batch(3)
        response = api_client_with_token.get(reverse('v1-users:user-list'))

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestUserDetailsView:
    def test_get_user_details(self, api_client):
        user = UserFactory()
        api_client.force_authenticate(user)

        response = api_client.get(reverse('v1-users:user-detail', args=(user.id,)))

        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == user.first_name

    def test_get_user_details_when_not_logged_it(self, api_client):
        user = UserFactory()

        response = api_client.get(reverse('v1-users:user-detail', args=(user.id,)))

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_user_details_not_found(self, api_client):
        api_client.force_authenticate(UserFactory.create_admin())

        response = api_client.get(reverse('v1-users:user-detail', args=(100,)))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_user_details_me_endpoint(self, api_client):
        user = UserFactory(first_name="John", last_name="Doe")
        api_client.force_authenticate(user)

        response = api_client.get(reverse('v1-users:user-me'))

        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == user.email
        assert response.data['first_name'] == user.first_name
        assert response.data['last_name'] == user.last_name
        assert response.data['city'] == user.city
        assert response.data['parish'] == user.parish
        assert response.data['community'] == user.community


@pytest.mark.django_db
class TestUserCreateView:
    def test_create_user(self, api_client):
        data = {'email': 'test@test.com', 'password': 'test123test123', 'confirm_password': 'test123test123'}

        response = api_client.post(reverse('v1-users:user-list'), data=data)
        user = User.objects.first()

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.all().count() == 1
        assert user.email == 'test@test.com'
        assert user.is_active is False

    def test_create_user_empty_password(self, api_client):
        data = {'email': 'test@test.com', 'password': '', 'confirm_password': ''}

        response = api_client.post(reverse('v1-users:user-list'), data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_user_password_not_match(self, api_client):
        data = {'email': 'test@test.com', 'password': 'test123test123', 'confirm_password': 'test123test'}

        response = api_client.post(reverse('v1-users:user-list'), data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_user_no_password(self, api_client):
        data = {'email': 'test@test.com'}

        response = api_client.post(reverse('v1-users:user-list'), data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserToken:
    sample_email = 'test@test.com'
    sample_password = 'test123test123'

    def create_user(self):
        user = UserFactory(email=self.sample_email)
        user.set_password(self.sample_password)
        user.save()

        return user

    def test_get_token(self, api_client):
        self.create_user()

        data = {'email': self.sample_email, 'password': self.sample_password}

        response = api_client.post(reverse('token_obtain_pair'), data=data)

        assert response.status_code == status.HTTP_200_OK
        assert 'refresh' in response.data
        assert 'access' in response.data

    def test_get_token_when_wrong_password(self, api_client):
        self.create_user()

        data = {'email': self.sample_email, 'password': 'test123'}

        response = api_client.post(reverse('token_obtain_pair'), data=data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_token_when_user_does_not_exist(self, api_client):
        data = {'email': 'test123@test.com', 'password': 'test123'}

        response = api_client.post(reverse('token_obtain_pair'), data=data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
