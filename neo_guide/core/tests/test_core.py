from django.urls import reverse
from rest_framework import status


def test_health_check_view(client):
    url = reverse('health-check')

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert b'It\'s working' in response.content


def test_redirect_to_admin_from_home(client):
    url = reverse('homepage')

    response = client.get(url, follow=True)

    assert response.status_code == status.HTTP_200_OK
    assert b'Log in' in response.content
