from locust import HttpUser
from locust import between

from neo_guide.load_tests.tasks.psalms_module import PsalmsModuleTaskSet
from neo_guide.load_tests.tasks.users_module import UsersModuleTaskSet


class NeoGuideWebUser(HttpUser):
    wait_time = between(5, 15)
    tasks = {PsalmsModuleTaskSet: 3, UsersModuleTaskSet: 1}
