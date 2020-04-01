import factory

from neo_guide.users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Sequence(lambda x: f'test.user.{x}@test.com')
    first_name = factory.Sequence(lambda x: f'first_name.test.{x}')
    last_name = factory.Sequence(lambda x: f'last_name.test.{x}')
    city = factory.Sequence(lambda x: f'City {x}')
    parish = factory.Sequence(lambda x: f'Parish {x}')
    community = factory.Sequence(lambda x: f'Community {x}')

    class Meta:
        model = User

    @classmethod
    def create_admin(cls):
        return cls(is_staff=True)
