import pytest
from django.db import IntegrityError

from neo_guide.users.tests.factories import UserFactory


@pytest.mark.django_db
class TestUserModel:
    def test_unique_email(self):
        email = 'test@test.com'

        with pytest.raises(IntegrityError):
            UserFactory.create_batch(2, email=email)
