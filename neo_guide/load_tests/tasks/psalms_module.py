import random

from locust import task

from neo_guide.load_tests.tasks.base import NeoGuideBaseTaskSet


class PsalmsModuleTaskSet(NeoGuideBaseTaskSet):
    PSALM_IDS = ['6', '7', '5', '4', '3', '10', '2', '8', '9']
    CARD_COLORS = ['white', 'yellow', 'green', 'blue', 'grey']
    PSALM_TYPES = ['peace_sign', 'fraction_of_bread', 'adoration', 'final_pslam', 'solid_pslams', 'penitential_liturgy']
    LITURGICAL_PERIOD = ['advent', 'christmas', 'lent', 'easter', 'normal_period']
    SEARCH_VALUES = ['zmar', 'anafo', 'mieszk', 'ma w nim']

    @task(10)
    def test_get_all_psalms(self):
        self.client.get(f'{self.HOST}/api/v1/psalms/')

    @task(8)
    def test_get_filtered_psalms_by_card_color(self):
        card_color = random.choice(self.CARD_COLORS)
        self.client.get(f'{self.HOST}/api/v1/psalms/?card_color={card_color}')

    @task(8)
    def test_get_filtered_psalms_by_type(self):
        psalm_type = random.choice(self.PSALM_TYPES)
        self.client.get(f'{self.HOST}/api/v1/psalms/?type={psalm_type}')

    @task(8)
    def test_get_filtered_psalms_by_liturgical_period(self):
        liturgical_period = random.choice(self.LITURGICAL_PERIOD)
        self.client.get(f'{self.HOST}/api/v1/psalms/?liturgical_period={liturgical_period}')

    @task(8)
    def test_get_filtered_psalms_by_search_value(self):
        search_value = random.choice(self.SEARCH_VALUES)
        self.client.get(f'{self.HOST}/api/v1/psalms/?search={search_value}')

    @task(5)
    def test_get_single_psalm(self):
        psalm_id = random.choice(self.PSALM_IDS)
        self.client.get(f'{self.HOST}/api/v1/psalms/{psalm_id}/')
