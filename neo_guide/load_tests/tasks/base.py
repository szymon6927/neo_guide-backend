from locust import TaskSet

from neo_guide.load_tests.config import LOCUST_HOST
from neo_guide.load_tests.config import LOCUST_USER_EMAIL
from neo_guide.load_tests.config import LOCUST_USER_PASSWORD


class LoadTestError(Exception):
    pass


class NeoGuideBaseTaskSet(TaskSet):
    _USER_DATA = {}
    HOST = LOCUST_HOST

    def _login(self):
        data = {'email': LOCUST_USER_EMAIL, 'password': LOCUST_USER_PASSWORD}
        response = self.client.post(f'{self.HOST}/api/v1/token/', data=data, name="[setup]/api/v1/token/")

        if not response.ok:
            raise LoadTestError(f"Can not get token! response={response.content}")

        token = response.json()['access']
        self.client.headers['Authorization'] = f'Bearer {token}'

    def _logout(self):
        self.client.headers['Authorization'] = ''

    def _fetch_user_data(self):
        response = self.client.get(f'{self.HOST}/api/v1/users/me', name="[setup]/api/v1/users/me")

        if not response.ok:
            raise LoadTestError(f"Can not fetch user info! response={response.content}")

        self.user_data = response.json()

    @property
    def user_data(self):
        return self._USER_DATA

    @user_data.setter
    def user_data(self, user_info):
        self._USER_DATA = user_info

    @property
    def host(self):
        return self.HOST

    def on_start(self):
        self._login()
        self._fetch_user_data()

    def on_stop(self):
        self._logout()
        self.user_data = {}
