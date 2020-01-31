import factory

from neo_guide.psalms.choices import CardColorChoices
from neo_guide.psalms.models import Psalm
from neo_guide.psalms.models import PsalmAudio
from neo_guide.psalms.models import PsalmImage


class PsalmFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda x: f'Psalm {x}')
    page_number = factory.Faker('pyint', min_value=0, max_value=500, step=1)
    card_color = factory.Faker('random_element', elements=[x[0] for x in CardColorChoices.choices])
    active = True

    class Meta:
        model = Psalm


class PsalmImageFactory(factory.django.DjangoModelFactory):
    image = factory.django.ImageField(color='blue')
    active = True
    default = False
    psalm = factory.SubFactory(PsalmFactory)

    class Meta:
        model = PsalmImage


class PsalmAudioFactory(factory.django.DjangoModelFactory):
    audio = factory.Faker('file_name', extension='mp3')
    active = True
    psalm = factory.SubFactory(PsalmFactory)

    class Meta:
        model = PsalmAudio
