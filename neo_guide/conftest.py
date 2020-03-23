import pytest
from pytest_django.lazy_django import skip_if_no_django
from rest_framework.test import APIClient

from neo_guide.psalms.choices import CardColorChoices
from neo_guide.psalms.choices import LiturgicalPeriodChoices
from neo_guide.psalms.choices import NeoStageChoices
from neo_guide.psalms.choices import PsalmTypeChoices
from neo_guide.psalms.tests.factories import PsalmFactory


@pytest.fixture()
def api_client():
    """A Django REST Framework api tests client instance."""
    skip_if_no_django()
    return APIClient()


@pytest.fixture()
def create_psalms_with_all_card_color_choices():
    PsalmFactory.create_batch(5, card_color=CardColorChoices.WHITE.value)
    PsalmFactory.create_batch(5, card_color=CardColorChoices.YELLOW.value)
    PsalmFactory.create_batch(5, card_color=CardColorChoices.GREEN.value)
    PsalmFactory.create_batch(5, card_color=CardColorChoices.BLUE.value)
    PsalmFactory.create_batch(5, card_color=CardColorChoices.GREY.value)


@pytest.fixture()
def create_psalms_with_all_psalm_type_choices():
    PsalmFactory.create_batch(5, type=PsalmTypeChoices.PEACE_SIGN.value)
    PsalmFactory.create_batch(5, type=PsalmTypeChoices.FRACTION_OF_BREAD.value)
    PsalmFactory.create_batch(5, type=PsalmTypeChoices.ADORATION.value)
    PsalmFactory.create_batch(5, type=PsalmTypeChoices.FINAL_PSALM.value)
    PsalmFactory.create_batch(5, type=PsalmTypeChoices.SOLID_PSALM.value)
    PsalmFactory.create_batch(5, type=PsalmTypeChoices.VIRGIN_MARY_PSALM.value)
    PsalmFactory.create_batch(5, type=PsalmTypeChoices.PENITENTIAL_LITURGY.value)


@pytest.fixture()
def create_psalms_with_all_liturgical_period_choices():
    PsalmFactory.create_batch(5, liturgical_period=LiturgicalPeriodChoices.ADVENT.value)
    PsalmFactory.create_batch(5, liturgical_period=LiturgicalPeriodChoices.LENT.value)
    PsalmFactory.create_batch(5, liturgical_period=LiturgicalPeriodChoices.EASTER.value)
    PsalmFactory.create_batch(5, liturgical_period=LiturgicalPeriodChoices.NORMAL_PERIOD.value)


@pytest.fixture()
def create_psalms_with_all_neo_stage_choices():
    PsalmFactory.create_batch(5, neo_stage=NeoStageChoices.FIRST_SCRUTINIUM.value)
    PsalmFactory.create_batch(5, neo_stage=NeoStageChoices.SHEMA.value)
    PsalmFactory.create_batch(5, neo_stage=NeoStageChoices.SECOND_SCRUTINIUM.value)
    PsalmFactory.create_batch(5, neo_stage=NeoStageChoices.INTRODUCTION_TO_PRAYER.value)
    PsalmFactory.create_batch(5, neo_stage=NeoStageChoices.TRADITIO.value)
    PsalmFactory.create_batch(5, neo_stage=NeoStageChoices.REDITIO.value)
    PsalmFactory.create_batch(5, neo_stage=NeoStageChoices.OUR_FATHER.value)
    PsalmFactory.create_batch(5, neo_stage=NeoStageChoices.CHOOSING.value)
    PsalmFactory.create_batch(5, neo_stage=NeoStageChoices.BAPTISM.value)
