import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from neo_guide.psalms.choices import CardColorChoices
from neo_guide.psalms.choices import LiturgicalPeriodChoices
from neo_guide.psalms.choices import NeoStageChoices
from neo_guide.psalms.choices import PsalmTypeChoices
from neo_guide.psalms.models import Psalm
from neo_guide.psalms.models import PsalmAudio
from neo_guide.psalms.models import PsalmImage
from neo_guide.psalms.tests.factories import PsalmAudioFactory
from neo_guide.psalms.tests.factories import PsalmFactory
from neo_guide.psalms.tests.factories import PsalmImageFactory


@pytest.mark.django_db
class TestPsalmListView:
    def test_get_psalms_when_no_audio_and_no_images(self, api_client_with_token):
        PsalmFactory.create_batch(3)
        response = api_client_with_token.get(reverse('v1-psalms:psalm-list'))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == Psalm.objects.count()

    def test_get_psalms_with_images(self, api_client_with_token):
        psalm = PsalmFactory()
        PsalmImageFactory(psalm=psalm)

        response = api_client_with_token.get(reverse('v1-psalms:psalm-list'))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == Psalm.objects.count()
        assert len(response.data['results'][0]['images']) == PsalmImage.objects.count()

    def test_get_psalms_with_audios(self, api_client_with_token):
        psalm = PsalmFactory()
        PsalmAudioFactory(psalm=psalm)

        response = api_client_with_token.get(reverse('v1-psalms:psalm-list'))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == Psalm.objects.count()
        assert len(response.data['results'][0]['recordings']) == PsalmAudio.objects.count()

    def test_get_psalms_when_not_logged_in(self, api_client):
        response = api_client.get(reverse('v1-psalms:psalm-list'))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPsalmListViewCardColorFilter:
    @pytest.mark.parametrize(
        "card_color, different_card_color, psalms_number",
        [
            (CardColorChoices.WHITE.value, CardColorChoices.YELLOW.value, 5),
            (CardColorChoices.YELLOW.value, CardColorChoices.WHITE.value, 5),
            (CardColorChoices.GREEN, CardColorChoices.WHITE.value, 5),
            (CardColorChoices.BLUE, CardColorChoices.GREY.value, 5),
            (CardColorChoices.GREY, CardColorChoices.BLUE.value, 5),
        ],
    )
    def test_card_color_filter_with_one_color(
        self, api_client_with_token, card_color, different_card_color, psalms_number
    ):
        PsalmFactory.create_batch(psalms_number, card_color=card_color)
        PsalmFactory.create_batch(psalms_number, card_color=different_card_color)

        response = api_client_with_token.get(reverse('v1-psalms:psalm-list'), {'card_color': card_color})
        assert Psalm.objects.all().count() == 2 * psalms_number
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == psalms_number
        assert response.data['count'] == psalms_number

    def test_card_color_filter_with_one_wrong_color(self, api_client_with_token):
        response = api_client_with_token.get(reverse('v1-psalms:psalm-list'), {'card_color': 'test'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'errors' in response.data
        assert response.data['errors'][0]['field'] == 'card_color'

    @pytest.mark.usefixtures("create_psalms_with_all_card_color_choices")
    @pytest.mark.parametrize(
        "card_colors, expected_result_number",
        [
            (f'{CardColorChoices.WHITE.value},{CardColorChoices.YELLOW.value}', 10),
            (f'{CardColorChoices.YELLOW.value},{CardColorChoices.WHITE.value}', 10),
            (f'{CardColorChoices.GREEN.value},{CardColorChoices.BLUE.value}', 10),
            (f'{CardColorChoices.WHITE.value},{CardColorChoices.GREY.value}', 10),
            (f'{CardColorChoices.YELLOW.value},{CardColorChoices.WHITE.value},{CardColorChoices.BLUE.value}', 15),
            (f'{CardColorChoices.WHITE.value},{CardColorChoices.GREEN.value},{CardColorChoices.BLUE.value}', 15),
            (f'{CardColorChoices.WHITE.value},{CardColorChoices.GREY.value},{CardColorChoices.BLUE.value}', 15),
            (
                f'{CardColorChoices.WHITE.value},{CardColorChoices.YELLOW.value},{CardColorChoices.GREEN.value},{CardColorChoices.BLUE.value}',
                20,
            ),
            (
                f'{CardColorChoices.WHITE.value},{CardColorChoices.YELLOW.value},{CardColorChoices.GREEN.value},{CardColorChoices.BLUE.value},{CardColorChoices.GREY.value}',
                25,
            ),
        ],
    )
    def test_card_color_filter_multiple_colors(self, api_client_with_token, card_colors, expected_result_number):
        assert Psalm.objects.all().count() == 25

        response = api_client_with_token.get(reverse('v1-psalms:psalm-list'), {'card_color': card_colors})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == expected_result_number
        assert response.data['count'] == expected_result_number

    @pytest.mark.usefixtures("create_psalms_with_all_card_color_choices")
    @pytest.mark.parametrize(
        "card_colors",
        [
            f'{CardColorChoices.WHITE.value},test'
            f'test,{CardColorChoices.BLUE.value}'
            f'{CardColorChoices.YELLOW.value},test,{CardColorChoices.BLUE.value}'
            f'{CardColorChoices.WHITE.value},test,test'
            f'test,{CardColorChoices.YELLOW.value},{CardColorChoices.GREEN.value},{CardColorChoices.BLUE.value}'
            f'{CardColorChoices.WHITE.value},{CardColorChoices.YELLOW.value},test,{CardColorChoices.BLUE.value}'
            f'{CardColorChoices.WHITE.value},test,test,{CardColorChoices.BLUE.value}'
        ],
    )
    def test_card_color_filter_multiple_colors_with_wrong_color(self, api_client_with_token, card_colors):

        assert Psalm.objects.all().count() == 25

        response = api_client_with_token.get(reverse('v1-psalms:psalm-list'), {'card_color': card_colors})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'errors' in response.data
        assert response.data['errors'][0]['field'] == 'card_color'


@pytest.mark.django_db
class TestPsalmListViewPsalmTypeFilter:
    @pytest.mark.parametrize(
        "psalm_type, different_psalm_type, psalms_number",
        [
            (PsalmTypeChoices.PEACE_SIGN.value, PsalmTypeChoices.FRACTION_OF_BREAD.value, 5),
            (PsalmTypeChoices.ADORATION.value, PsalmTypeChoices.FINAL_PSALM.value, 5),
            (PsalmTypeChoices.SOLID_PSALM.value, PsalmTypeChoices.VIRGIN_MARY_PSALM.value, 5),
            (PsalmTypeChoices.VIRGIN_MARY_PSALM.value, PsalmTypeChoices.PENITENTIAL_LITURGY.value, 5),
        ],
    )
    def test_psalm_type_filter_with_one_type(
        self, api_client_with_token, psalm_type, different_psalm_type, psalms_number
    ):
        PsalmFactory.create_batch(psalms_number, type=psalm_type)
        PsalmFactory.create_batch(psalms_number, type=different_psalm_type)

        response = api_client_with_token.get(reverse('v1-psalms:psalm-list'), {'type': psalm_type})
        assert Psalm.objects.all().count() == 2 * psalms_number
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == psalms_number
        assert response.data['count'] == psalms_number

    def test_psalm_type_filter_with_one_wrong_type(self, api_client_with_token):
        response = api_client_with_token.get(reverse('v1-psalms:psalm-list'), {'type': 'test'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'errors' in response.data
        assert response.data['errors'][0]['field'] == 'type'

    @pytest.mark.usefixtures("create_psalms_with_all_psalm_type_choices")
    @pytest.mark.parametrize(
        "psalm_types, expected_result_number",
        [
            (f'{PsalmTypeChoices.PEACE_SIGN.value},{PsalmTypeChoices.FRACTION_OF_BREAD.value}', 10),
            (f'{PsalmTypeChoices.ADORATION.value},{PsalmTypeChoices.FINAL_PSALM.value}', 10),
            (f'{PsalmTypeChoices.SOLID_PSALM.value},{PsalmTypeChoices.VIRGIN_MARY_PSALM.value}', 10),
            (f'{PsalmTypeChoices.VIRGIN_MARY_PSALM.value},{PsalmTypeChoices.PENITENTIAL_LITURGY.value}', 10),
            (
                f'{PsalmTypeChoices.PEACE_SIGN.value},{PsalmTypeChoices.FRACTION_OF_BREAD.value},{PsalmTypeChoices.ADORATION.value}',
                15,
            ),
        ],
    )
    def test_psalm_type_filter_multiple_types(self, api_client_with_token, psalm_types, expected_result_number):
        assert Psalm.objects.all().count() == 35

        response = api_client_with_token.get(reverse('v1-psalms:psalm-list'), {'type': psalm_types})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == expected_result_number
        assert response.data['count'] == expected_result_number

    @pytest.mark.usefixtures("create_psalms_with_all_psalm_type_choices")
    @pytest.mark.parametrize(
        "psalm_types, expected_result_number",
        [
            (f'{PsalmTypeChoices.VIRGIN_MARY_PSALM.value},test', 10),
            (f'test,{PsalmTypeChoices.PENITENTIAL_LITURGY.value}', 10),
            (f'{PsalmTypeChoices.FRACTION_OF_BREAD.value},test,{PsalmTypeChoices.PENITENTIAL_LITURGY.value}', 15),
            (f'{PsalmTypeChoices.VIRGIN_MARY_PSALM.value},test,test', 15),
        ],
    )
    def test_psalm_type_filter_multiple_colors_with_wrong_color(
        self, api_client_with_token, psalm_types, expected_result_number
    ):
        assert Psalm.objects.all().count() == 35

        response = api_client_with_token.get(reverse('v1-psalms:psalm-list'), {'type': psalm_types})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'errors' in response.data
        assert response.data['errors'][0]['field'] == 'type'


@pytest.mark.django_db
class TestPsalmListViewLiturgicalPeriodFilter:
    @pytest.mark.parametrize(
        "liturgical_period, different_liturgical_period, psalms_number",
        [
            (LiturgicalPeriodChoices.CHRISTMAS.value, LiturgicalPeriodChoices.ADVENT.value, 5),
            (LiturgicalPeriodChoices.ADVENT.value, LiturgicalPeriodChoices.LENT.value, 5),
            (LiturgicalPeriodChoices.EASTER.value, LiturgicalPeriodChoices.NORMAL_PERIOD.value, 5),
        ],
    )
    def test_liturgical_period_filter_with_one_type(
        self, api_client_with_token, liturgical_period, different_liturgical_period, psalms_number
    ):
        PsalmFactory.create_batch(psalms_number, liturgical_period=liturgical_period)
        PsalmFactory.create_batch(psalms_number, liturgical_period=different_liturgical_period)

        response = api_client_with_token.get(reverse('v1-psalms:psalm-list'), {'liturgical_period': liturgical_period})
        assert Psalm.objects.all().count() == 2 * psalms_number
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == psalms_number
        assert response.data['count'] == psalms_number

    def test_liturgical_period_filter_with_one_wrong_type(self, api_client_with_token):
        response = api_client_with_token.get(reverse('v1-psalms:psalm-list'), {'liturgical_period': 'test'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'errors' in response.data
        assert response.data['errors'][0]['field'] == 'liturgical_period'

    @pytest.mark.usefixtures("create_psalms_with_all_liturgical_period_choices")
    @pytest.mark.parametrize(
        "liturgical_periods, expected_result_number",
        [
            (f'{LiturgicalPeriodChoices.ADVENT.value},{LiturgicalPeriodChoices.CHRISTMAS.value}', 10),
            (f'{LiturgicalPeriodChoices.ADVENT.value},{LiturgicalPeriodChoices.LENT.value}', 10),
            (f'{LiturgicalPeriodChoices.EASTER.value},{LiturgicalPeriodChoices.NORMAL_PERIOD.value}', 10),
            (
                f'{LiturgicalPeriodChoices.ADVENT.value},{LiturgicalPeriodChoices.LENT.value},{LiturgicalPeriodChoices.EASTER.value}',
                15,
            ),
        ],
    )
    def test_liturgical_period_filter_multiple_types(
        self, api_client_with_token, liturgical_periods, expected_result_number
    ):
        assert Psalm.objects.all().count() == 25

        response = api_client_with_token.get(reverse('v1-psalms:psalm-list'), {'liturgical_period': liturgical_periods})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == expected_result_number
        assert response.data['count'] == expected_result_number

    @pytest.mark.usefixtures("create_psalms_with_all_liturgical_period_choices")
    @pytest.mark.parametrize(
        "liturgical_periods",
        [
            f'{LiturgicalPeriodChoices.ADVENT.value},test',
            f'test,{LiturgicalPeriodChoices.LENT.value}',
            f'{LiturgicalPeriodChoices.EASTER.value},test,{LiturgicalPeriodChoices.NORMAL_PERIOD.value}',
            f'{LiturgicalPeriodChoices.CHRISTMAS.value},test,test',
        ],
    )
    def test_liturgical_period_filter_multiple_colors_with_wrong_color(self, api_client_with_token, liturgical_periods):
        assert Psalm.objects.all().count() == 25

        response = api_client_with_token.get(reverse('v1-psalms:psalm-list'), {'liturgical_period': liturgical_periods})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'errors' in response.data
        assert response.data['errors'][0]['field'] == 'liturgical_period'


@pytest.mark.django_db
class TestPsalmListViewNeoStageFilter:
    @pytest.mark.parametrize(
        "neo_stage, different_neo_stage, psalms_number",
        [
            (NeoStageChoices.PRE_CATECHUMENATE.value, NeoStageChoices.FIRST_SCRUTINIUM, 5),
            (NeoStageChoices.FIRST_SCRUTINIUM.value, NeoStageChoices.SHEMA.value, 5),
            (NeoStageChoices.SECOND_SCRUTINIUM.value, NeoStageChoices.INTRODUCTION_TO_PRAYER.value, 5),
            (NeoStageChoices.TRADITIO.value, NeoStageChoices.REDITIO.value, 5),
            (NeoStageChoices.OUR_FATHER.value, NeoStageChoices.CHOOSING.value, 5),
            (NeoStageChoices.BAPTISM.value, NeoStageChoices.FIRST_SCRUTINIUM.value, 5),
        ],
    )
    def test_neo_stage_filter_with_one_type(self, api_client_with_token, neo_stage, different_neo_stage, psalms_number):
        PsalmFactory.create_batch(psalms_number, neo_stage=neo_stage)
        PsalmFactory.create_batch(psalms_number, neo_stage=different_neo_stage)

        response = api_client_with_token.get(reverse('v1-psalms:psalm-list'), {'neo_stage': neo_stage})
        assert Psalm.objects.all().count() == 2 * psalms_number
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == psalms_number
        assert response.data['count'] == psalms_number

    def test_neo_stage_filter_with_one_wrong_type(self, api_client_with_token):
        response = api_client_with_token.get(reverse('v1-psalms:psalm-list'), {'neo_stage': 'test'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'errors' in response.data
        assert response.data['errors'][0]['field'] == 'neo_stage'

    @pytest.mark.usefixtures("create_psalms_with_all_neo_stage_choices")
    @pytest.mark.parametrize(
        "neo_stages, expected_result_number",
        [
            (f'{NeoStageChoices.PRE_CATECHUMENATE.value}, {NeoStageChoices.SECOND_SCRUTINIUM.value}', 10),
            (f'{NeoStageChoices.FIRST_SCRUTINIUM.value}, {NeoStageChoices.SHEMA.value}', 10),
            (f'{NeoStageChoices.SECOND_SCRUTINIUM.value}, {NeoStageChoices.INTRODUCTION_TO_PRAYER.value}', 10),
            (f'{NeoStageChoices.TRADITIO.value}, {NeoStageChoices.REDITIO.value}', 10),
            (f'{NeoStageChoices.OUR_FATHER.value}, {NeoStageChoices.CHOOSING.value}', 10),
            (
                f'{NeoStageChoices.BAPTISM.value}, {NeoStageChoices.FIRST_SCRUTINIUM.value}, {NeoStageChoices.SHEMA.value}',
                15,
            ),
        ],
    )
    def test_neo_stage_filter_multiple_types(self, api_client_with_token, neo_stages, expected_result_number):
        assert Psalm.objects.all().count() == 50

        response = api_client_with_token.get(reverse('v1-psalms:psalm-list'), {'neo_stage': neo_stages})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == expected_result_number
        assert response.data['count'] == expected_result_number

    @pytest.mark.usefixtures("create_psalms_with_all_neo_stage_choices")
    @pytest.mark.parametrize(
        "neo_stages",
        [
            f'{NeoStageChoices.FIRST_SCRUTINIUM.value},test',
            f'test,{NeoStageChoices.SHEMA.value}',
            f'{NeoStageChoices.SECOND_SCRUTINIUM.value},test,{NeoStageChoices.INTRODUCTION_TO_PRAYER.value}',
            f'{NeoStageChoices.TRADITIO.value},test,test',
        ],
    )
    def test_neo_stage_filter_with_wrong_stage(self, api_client_with_token, neo_stages):
        assert Psalm.objects.all().count() == 50

        response = api_client_with_token.get(reverse('v1-psalms:psalm-list'), {'neo_stage': neo_stages})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'errors' in response.data
        assert response.data['errors'][0]['field'] == 'neo_stage'


@pytest.mark.django_db
class TestPsalmListViewWithMultipleFilters:
    def test_multiple_filters_scenario_1(self, api_client_with_token):
        PsalmFactory.create_batch(
            5,
            card_color=CardColorChoices.WHITE.value,
            type=PsalmTypeChoices.PEACE_SIGN.value,
            liturgical_period=LiturgicalPeriodChoices.NORMAL_PERIOD.value,
        )

        response = api_client_with_token.get(
            reverse('v1-psalms:psalm-list'),
            {
                'card_color': CardColorChoices.WHITE.value,
                'type': PsalmTypeChoices.PEACE_SIGN.value,
                'liturgical_period': LiturgicalPeriodChoices.NORMAL_PERIOD.value,
            },
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 5
        assert response.data['count'] == 5

    def test_multiple_filters_scenario_2(self, api_client_with_token):
        PsalmFactory.create_batch(
            5,
            card_color=CardColorChoices.WHITE.value,
            type=PsalmTypeChoices.PEACE_SIGN.value,
            neo_stage=NeoStageChoices.FIRST_SCRUTINIUM.value,
        )

        response = api_client_with_token.get(
            reverse('v1-psalms:psalm-list'),
            {
                'card_color': CardColorChoices.WHITE.value,
                'type': PsalmTypeChoices.PEACE_SIGN.value,
                'neo_stage': NeoStageChoices.FIRST_SCRUTINIUM.value,
            },
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 5
        assert response.data['count'] == 5

    def test_multiple_filters_scenario_3(self, api_client_with_token):
        PsalmFactory.create_batch(5, card_color=CardColorChoices.WHITE.value, type=PsalmTypeChoices.PEACE_SIGN.value)

        PsalmFactory.create_batch(5, card_color=CardColorChoices.BLUE.value, type=PsalmTypeChoices.PEACE_SIGN.value)

        response = api_client_with_token.get(
            reverse('v1-psalms:psalm-list'),
            {
                'card_color': f'{CardColorChoices.WHITE.value}, {CardColorChoices.BLUE.value}',
                'type': PsalmTypeChoices.PEACE_SIGN.value,
            },
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 10
        assert response.data['count'] == 10


@pytest.mark.django_db
class TestPsalmDetailsView:
    def test_get_psalm_details(self, api_client_with_token):
        psalm = PsalmFactory()

        response = api_client_with_token.get(reverse('v1-psalms:psalm-detail', args=(psalm.id,)))

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == psalm.name

    def test_get_psalm_details_not_found(self, api_client_with_token):
        response = api_client_with_token.get(reverse('v1-psalms:psalm-detail', args=(100,)))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_psalm_default_image(self, api_client_with_token):
        psalm = PsalmFactory()
        PsalmImageFactory(psalm=psalm, default=True)

        response = api_client_with_token.get(reverse('v1-psalms:psalm-detail', args=(psalm.id,)))

        assert response.status_code == status.HTTP_200_OK
        assert response.data['default_image'] is not None

    def test_get_psalm_without_default_image(self, api_client_with_token):
        psalm = PsalmFactory()
        PsalmImageFactory(psalm=psalm)

        response = api_client_with_token.get(reverse('v1-psalms:psalm-detail', args=(psalm.id,)))

        assert response.status_code == status.HTTP_200_OK
        assert response.data['default_image'] is None

    def test_get_psalm_details_with_images(self, api_client_with_token):
        psalm = PsalmFactory()
        PsalmImageFactory.create_batch(5, psalm=psalm)

        response = api_client_with_token.get(reverse('v1-psalms:psalm-detail', args=(psalm.id,)))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['images']) == PsalmImage.objects.count()

    def test_get_psalm_details_without_images(self, api_client_with_token):
        psalm = PsalmFactory()

        response = api_client_with_token.get(reverse('v1-psalms:psalm-detail', args=(psalm.id,)))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['images']) == PsalmImage.objects.count()

    def test_get_psalm_details_with_recordings(self, api_client_with_token):
        psalm = PsalmFactory()
        PsalmAudioFactory.create_batch(5, psalm=psalm)

        response = api_client_with_token.get(reverse('v1-psalms:psalm-detail', args=(psalm.id,)))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['recordings']) == PsalmAudio.objects.count()

    def test_get_psalm_details_without_recordings(self, api_client_with_token):
        psalm = PsalmFactory()

        response = api_client_with_token.get(reverse('v1-psalms:psalm-detail', args=(psalm.id,)))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['recordings']) == PsalmAudio.objects.count()

    def test_get_psalm_when_not_logged_in(self, api_client):
        psalm = PsalmFactory()

        response = api_client.get(reverse('v1-psalms:psalm-detail', args=(psalm.id,)))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
