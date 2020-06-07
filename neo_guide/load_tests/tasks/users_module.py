import random

from locust import task

from neo_guide.load_tests.tasks.base import NeoGuideBaseTaskSet


class UsersModuleTaskSet(NeoGuideBaseTaskSet):
    @task(3)
    def test_get_user(self):
        self.client.get(f'{self.HOST}/api/v1/users/me')

    @task(1)
    def test_change_user_data(self):
        random_number = random.randint(1, 100)

        user_data = self.user_data
        user_id = user_data['id']
        user_data['city'] = f'City {random_number}'
        user_data['parish'] = f'Parish {random_number}'
        user_data['community'] = f'Community {random_number}'

        self.client.put(f'{self.HOST}/api/v1/users/{user_id}/', user_data)
